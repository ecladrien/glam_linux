from __future__ import annotations
from typing import List, Optional
import logging
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from ipaddress import ip_address
from urllib.parse import quote

import cv2
try:
    from onvif import ONVIFCamera
except Exception:
    ONVIFCamera = None


from ..config.manager import Config

logger = logging.getLogger(__name__)


class CameraService:
    def __init__(self, config: Config):
        self.config = config
        self._onvif_client = None
        self._ptz_service = None
        self._media_service = None
        self._profile_token = None

    def _safe_str(self, value) -> str:
        if value is None:
            return ""
        if hasattr(value, "get_secret_value"):
            try:
                return str(value.get_secret_value())
            except Exception:
                return str(value)
        return str(value)

    def _resolve_base_ip(self, preferred_ip: Optional[str] = None) -> str:
        candidates = [
            preferred_ip,
            getattr(self.config.network, "camera_ip", None),
            getattr(self.config.network, "device_ip", None),
            self._get_local_ip(),
        ]
        for candidate in candidates:
            if not candidate:
                continue
            try:
                ip_address(str(candidate))
                return str(candidate)
            except Exception:
                continue
        return "192.168.1.1"

    def _get_local_ip(self) -> str:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
        except Exception:
            return "127.0.0.1"
        finally:
            sock.close()

    def _probe_tcp_port(self, ip: str, port: int, timeout: float = 0.35) -> bool:
        try:
            with socket.create_connection((ip, port), timeout=timeout):
                return True
        except Exception:
            return False

    def scan_subnet_for_rtsp(self, base_ip: str, limit: int = 254, timeout: float = 0.35) -> List[str]:
        """Scan le sous-réseau de `base_ip` pour détecter des hôtes avec port RTSP ouvert."""
        try:
            octets = str(base_ip).split(".")
            prefix = ".".join(octets[:3])
        except Exception:
            logger.exception("Invalid base IP for scan: %s", base_ip)
            return []

        current_ip = self._resolve_base_ip(base_ip)
        to_scan = []
        for host in range(1, int(limit) + 1):
            ip = f"{prefix}.{host}"
            if ip == current_ip:
                continue
            to_scan.append(ip)

        found: List[str] = []
        max_workers = min(64, max(8, len(to_scan) // 4))
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {pool.submit(self._probe_tcp_port, ip, 554, timeout): ip for ip in to_scan}
            for future in as_completed(futures):
                ip = futures[future]
                try:
                    if future.result():
                        found.append(ip)
                except Exception:
                    logger.debug("Scan probe failed for %s", ip, exc_info=True)

        found.sort(key=lambda x: tuple(int(part) for part in x.split(".")))
        return found

    def _onvif_ping(self, ip: str, timeout: float = 1.0) -> bool:
        """Retourne True si la caméra répond sur le port ONVIF configuré."""
        port = int(getattr(self.config.camera, "onvif_port", 8000))
        return self._probe_tcp_port(ip, port, timeout=timeout)

    def _rtsp_url_candidates(self, ip: str) -> List[str]:
        user = quote(self._safe_str(getattr(self.config.camera, "rtsp_user", "")), safe="")
        password = quote(self._safe_str(getattr(self.config.camera, "rtsp_password", "")), safe="")
        configured_stream = str(getattr(self.config.camera, "rtsp_stream", "/h264Preview_01_main") or "")

        stream_paths = [
            configured_stream,
            "/h264Preview_01_main",
            "/h264Preview_01_sub",
            "/h265Preview_01_main",
        ]
        normalized_paths = []
        for path in stream_paths:
            p = str(path).strip()
            if not p:
                continue
            if not p.startswith("/"):
                p = f"/{p}"
            if p not in normalized_paths:
                normalized_paths.append(p)

        auth = f"{user}:{password}@" if user else ""
        return [f"rtsp://{auth}{ip}:554{path}" for path in normalized_paths]

    def build_rtsp_url(self, ip: str) -> str:
        """Construit l'URL RTSP principale pour une caméra donnée."""
        candidates = self._rtsp_url_candidates(ip)
        return candidates[0] if candidates else f"rtsp://{ip}:554/h264Preview_01_main"

    def probe_rtsp_url(self, url: str, timeout_ms: int = 1800) -> bool:
        cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
        if not cap.isOpened():
            cap.release()
            return False

        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, timeout_ms)
        cap.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, timeout_ms)
        ok, frame = cap.read()
        cap.release()
        return bool(ok and frame is not None and frame.size > 0)

    def find_working_rtsp_url(self, ip: str) -> Optional[str]:
        for url in self._rtsp_url_candidates(ip):
            try:
                if self.probe_rtsp_url(url):
                    return url
            except Exception:
                logger.debug("RTSP probe failed for %s", url, exc_info=True)
        return None

    def discover_cameras(self, preferred_ip: Optional[str] = None) -> List[str]:
        """Découvre les caméras RTSP/ONVIF du sous-réseau local.

        - Scan rapide port RTSP 554
        - Priorise l'IP connue depuis la config
        - Garde les hôtes répondant RTSP ou ONVIF
        """
        base_ip = self._resolve_base_ip(preferred_ip)
        candidates = self.scan_subnet_for_rtsp(base_ip)

        priority_ip = preferred_ip or getattr(self.config.network, "camera_ip", None)
        if priority_ip:
            priority_ip = str(priority_ip)
            if priority_ip not in candidates:
                candidates.insert(0, priority_ip)
            else:
                candidates = [priority_ip] + [ip for ip in candidates if ip != priority_ip]

        if not candidates:
            return []

        validated: List[str] = []
        for ip in candidates:
            try:
                if self._probe_tcp_port(ip, 554, timeout=0.35) or self._onvif_ping(ip, timeout=0.5):
                    validated.append(ip)
            except Exception:
                logger.debug("Candidate validation failed for %s", ip, exc_info=True)

        deduped = []
        for ip in validated:
            if ip not in deduped:
                deduped.append(ip)
        return deduped

    def _init_onvif(self, ip: str) -> bool:
        if ONVIFCamera is None:
            logger.warning("ONVIF dependency unavailable; install onvif_zeep")
            return False

        user = self._safe_str(getattr(self.config.camera, "rtsp_user", ""))
        password = self._safe_str(getattr(self.config.camera, "rtsp_password", ""))
        port = int(getattr(self.config.camera, "onvif_port", 8000))

        try:
            self._onvif_client = ONVIFCamera(ip, port, user, password)
            self._media_service = self._onvif_client.create_media_service()
            self._ptz_service = self._onvif_client.create_ptz_service()

            profiles = self._media_service.GetProfiles()
            if not profiles:
                logger.warning("No ONVIF profile found for %s", ip)
                return False

            self._profile_token = profiles[0].token
            return True
        except Exception:
            logger.exception("Failed to initialize ONVIF for %s", ip)
            self._onvif_client = None
            self._media_service = None
            self._ptz_service = None
            self._profile_token = None
            return False

    def _ensure_onvif_ready(self, ip: str) -> bool:
        if self._ptz_service is not None and self._profile_token is not None:
            return True
        return self._init_onvif(ip)

    def _continuous_zoom(self, ip: str, velocity: float) -> bool:
        """Apply ONVIF ContinuousZoom using PTZ service.

        Positive velocity zooms in, negative zooms out.
        """
        if not self._ensure_onvif_ready(ip):
            return False

        try:
            request = self._ptz_service.create_type("ContinuousMove")
            request.ProfileToken = self._profile_token
            request.Velocity = {
                "Zoom": {
                    "x": float(velocity),
                }
            }
            self._ptz_service.ContinuousMove(request)
            time.sleep(0.25)

            stop_request = self._ptz_service.create_type("Stop")
            stop_request.ProfileToken = self._profile_token
            stop_request.PanTilt = False
            stop_request.Zoom = True
            self._ptz_service.Stop(stop_request)
            return True
        except Exception:
            logger.exception("Failed to apply camera zoom on %s", ip)
            return False

    def zoom_in(self, ip: str, speed: float = 0.5) -> bool:
        speed = max(0.1, min(1.0, float(speed)))
        return self._continuous_zoom(ip, speed)

    def zoom_out(self, ip: str, speed: float = 0.5) -> bool:
        speed = max(0.1, min(1.0, float(speed)))
        return self._continuous_zoom(ip, -speed)
