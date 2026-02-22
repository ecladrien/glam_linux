from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any, Optional
import shutil
import logging

from ..config.manager import Config

logger = logging.getLogger(__name__)


class SetupService:
    """Service pour opérations liées à la page de configuration.

    Opérations prises en charge:
    - lecture/écriture des valeurs de configuration (sans UI)
    - restauration des valeurs par défaut
    - ajout/suppression de plans (copie / suppression de fichiers)
    - mise à jour de l'image d'entête
    """

    def __init__(self, config: Config):
        self.config = config

    def get_config_values(self) -> Dict[str, Any]:
        return {
            "screen_width": int(self.config.display.screen_width),
            "screen_height": int(self.config.display.screen_height),
            "fullscreen": bool(self.config.display.fullscreen),
            "device_ip": str(getattr(self.config.network, 'device_ip', '')),
            "camera_ip": str(getattr(self.config.network, 'camera_ip', '')),
            "artnet_network": str(getattr(self.config.network, 'artnet_network', '')),
            "onvif_port": int(getattr(self.config.camera, 'onvif_port', 0)),
            "rtsp_user": str(getattr(self.config.camera, 'rtsp_user', '')),
            "rtsp_password": str(getattr(self.config.camera, 'rtsp_password', '')),
        }

    def save_config_values(self, values: Dict[str, Any]) -> None:
        # Assign into nested config and persist
        try:
            self.config.display.screen_width = int(values.get('screen_width', self.config.display.screen_width))
            self.config.display.screen_height = int(values.get('screen_height', self.config.display.screen_height))
            self.config.display.fullscreen = bool(values.get('fullscreen', self.config.display.fullscreen))
            self.config.network.device_ip = values.get('device_ip', self.config.network.device_ip)
            self.config.network.camera_ip = values.get('camera_ip', self.config.network.camera_ip)
            self.config.network.artnet_network = values.get('artnet_network', self.config.network.artnet_network)
            self.config.camera.onvif_port = int(values.get('onvif_port', self.config.camera.onvif_port))
            self.config.camera.rtsp_user = values.get('rtsp_user', self.config.camera.rtsp_user)
            self.config.camera.rtsp_password = values.get('rtsp_password', self.config.camera.rtsp_password)
            self.config.save()
        except Exception:
            logger.exception('Failed to save configuration')
            raise

    def reset_to_defaults(self) -> None:
        default = Config()
        self.config.display.screen_width = default.display.screen_width
        self.config.display.screen_height = default.display.screen_height
        self.config.display.fullscreen = default.display.fullscreen
        self.config.network.device_ip = default.network.device_ip
        self.config.network.camera_ip = default.network.camera_ip
        self.config.network.artnet_network = default.network.artnet_network
        self.config.camera.onvif_port = default.camera.onvif_port
        self.config.camera.rtsp_user = default.camera.rtsp_user
        self.config.camera.rtsp_password = default.camera.rtsp_password

    def add_plans(self, file_paths: List[Path]) -> Dict[str, Any]:
        """Copy provided files into the configured plan_dir.

        Returns a dict with keys: count_copied, target_dir
        """
        target_dir = Path(self.config.paths.plan_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        copied = 0
        for f in file_paths:
            src = Path(f)
            if not src.exists():
                logger.warning('Selected file not found: %s', src)
                continue

            dest = target_dir / src.name
            if dest.exists():
                stem = src.stem
                suffix = src.suffix
                i = 1
                while True:
                    candidate = target_dir / f"{stem}_{i}{suffix}"
                    if not candidate.exists():
                        dest = candidate
                        break
                    i += 1

            try:
                shutil.copy2(src, dest)
                copied += 1
            except Exception:
                logger.exception('Failed copying plan %s to %s', src, dest)

        return {"count_copied": copied, "target_dir": target_dir}

    def delete_plans(self, file_paths: List[Path]) -> Dict[str, Any]:
        target_dir = Path(self.config.paths.plan_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        deleted = 0
        total = len(file_paths)
        for f in file_paths:
            p = Path(f)
            try:
                if p.exists():
                    p.unlink()
                    deleted += 1
                else:
                    logger.warning('File not found during deletion: %s', p)
            except Exception:
                logger.exception('Error deleting file: %s', p)

        return {"deleted": deleted, "total": total, "target_dir": target_dir}

    def set_head_image(self, path: Path) -> None:
        try:
            self.config.paths.head_img = path
            self.config.save()
        except Exception:
            logger.exception('Failed to set head image')
            raise
