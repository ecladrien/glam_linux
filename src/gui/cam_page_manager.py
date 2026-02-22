from __future__ import annotations

import logging
import threading

import cv2
import numpy as np
from PySide6.QtCore import QObject, Qt, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout

from ..config.manager import Config
from ..services.camera_service import CameraService

logger = logging.getLogger(__name__)


class FullscreenVideoLabel(QLabel):
    clicked = Signal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        event.accept()


class CamSignals(QObject):
    frame_ready = Signal(np.ndarray)
    status_changed = Signal(str)
    connect_enabled = Signal(bool)
    disconnect_enabled = Signal(bool)


class CamPageManager:
    """Gestion optimisée de la page caméra.

    - Utilise `connect_cam_button` pour lancer la découverte/connexion
    - Utilise `flux_video_label` pour afficher le flux vidéo
    """

    def __init__(self, main_window, config: Config):
        self.main_window = main_window
        self.config = config
        self.ui = main_window.ui
        self.camera_service = CameraService(config)

        self._signals = CamSignals()
        self._signals.frame_ready.connect(self._on_frame_ready)
        self._signals.status_changed.connect(self._on_status_changed)
        self._signals.connect_enabled.connect(self._set_connect_button_enabled)
        self._signals.disconnect_enabled.connect(self._set_disconnect_button_enabled)

        self._stream_stop = threading.Event()
        self._stream_thread: threading.Thread | None = None
        self._connect_thread: threading.Thread | None = None
        self.current_camera_ip: str | None = None
        self._last_pixmap: QPixmap | None = None

        self._fullscreen_window: QWidget | None = None
        self._fullscreen_label: FullscreenVideoLabel | None = None

        self._init_video_label()
        self._bind_ui()
        self._signals.disconnect_enabled.emit(False)

        try:
            self.main_window.destroyed.connect(lambda *_: self.stop_stream())
        except Exception:
            logger.debug("Could not bind camera cleanup on main window destroy")

    def _bind_ui(self) -> None:
        connect_button = getattr(self.ui, "connect_cam_button", None)
        if connect_button is None:
            logger.debug("connect_cam_button not found in UI")
            return
        connect_button.clicked.connect(self._on_connect_clicked)

        disconnect_button = getattr(self.ui, "disconnect_cam_button", None)
        if disconnect_button is None:
            logger.debug("disconnect_cam_button not found in UI")
            return
        disconnect_button.clicked.connect(self._on_disconnect_clicked)

        plus_zoom_button = getattr(self.ui, "plus_zoom_cam_button", None)
        if plus_zoom_button is not None:
            plus_zoom_button.clicked.connect(self._on_zoom_in_clicked)
        else:
            logger.debug("plus_zoom_cam_button not found in UI")

        minus_zoom_button = getattr(self.ui, "minus_zoom_cam_button", None)
        if minus_zoom_button is not None:
            minus_zoom_button.clicked.connect(self._on_zoom_out_clicked)
        else:
            logger.debug("minus_zoom_cam_button not found in UI")

        fullscreen_button = getattr(self.ui, "full_screen_cam_button", None)
        if fullscreen_button is not None:
            fullscreen_button.clicked.connect(self._on_fullscreen_clicked)
        else:
            logger.debug("full_screen_cam_button not found in UI")

    def _init_video_label(self) -> None:
        label = self._video_label
        if label is None:
            logger.debug("flux_video_label not found in UI")
            return
        label.setAlignment(Qt.AlignCenter)
        label.setText("Cliquez sur connecter pour rechercher la caméra")

    def _clear_video_label(self, message: str) -> None:
        label = self._video_label
        if label is None:
            return
        label.clear()
        label.setText(message)

    @property
    def _video_label(self) -> QLabel | None:
        label = getattr(self.ui, "flux_video_label", None)
        return label if isinstance(label, QLabel) else None

    def _on_connect_clicked(self) -> None:
        if self._stream_thread is not None and self._stream_thread.is_alive():
            self.stop_stream()
            self._clear_video_label("Flux caméra arrêté")
            self._signals.status_changed.emit("Flux caméra arrêté")
            return

        if self._connect_thread is not None and self._connect_thread.is_alive():
            self._signals.status_changed.emit("Connexion caméra en cours...")
            return

        self._connect_thread = threading.Thread(target=self._connect_worker, daemon=True)
        self._connect_thread.start()

    def _on_disconnect_clicked(self) -> None:
        self.stop_stream()
        self._clear_video_label("Caméra déconnectée")
        self._signals.status_changed.emit("Caméra déconnectée")

    def _on_zoom_in_clicked(self) -> None:
        if not self.current_camera_ip:
            self._signals.status_changed.emit("Aucune caméra active pour zoom +")
            return
        ok = self.camera_service.zoom_in(self.current_camera_ip)
        self._signals.status_changed.emit("Zoom +" if ok else "Échec zoom +")

    def _on_zoom_out_clicked(self) -> None:
        if not self.current_camera_ip:
            self._signals.status_changed.emit("Aucune caméra active pour zoom -")
            return
        ok = self.camera_service.zoom_out(self.current_camera_ip)
        self._signals.status_changed.emit("Zoom -" if ok else "Échec zoom -")

    def _on_fullscreen_clicked(self) -> None:
        if self._fullscreen_window is not None and self._fullscreen_window.isVisible():
            self._exit_fullscreen()
            return

        label = self._video_label
        if label is None:
            self._signals.status_changed.emit("Label vidéo indisponible")
            return

        self._fullscreen_window = QWidget()
        self._fullscreen_window.setWindowTitle("Flux caméra")
        self._fullscreen_window.setStyleSheet("background-color: black;")

        layout = QVBoxLayout(self._fullscreen_window)
        layout.setContentsMargins(0, 0, 0, 0)

        self._fullscreen_label = FullscreenVideoLabel(self._fullscreen_window)
        self._fullscreen_label.setAlignment(Qt.AlignCenter)
        self._fullscreen_label.setStyleSheet("background-color: black;")
        self._fullscreen_label.clicked.connect(self._exit_fullscreen)
        layout.addWidget(self._fullscreen_label)

        if self._last_pixmap is not None:
            self._set_fullscreen_pixmap(self._last_pixmap)
        else:
            self._fullscreen_label.setText("Aucune image vidéo")

        self._fullscreen_window.showFullScreen()

    def _set_fullscreen_pixmap(self, pixmap: QPixmap) -> None:
        if self._fullscreen_label is None:
            return
        scaled = pixmap.scaled(
            self._fullscreen_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self._fullscreen_label.setPixmap(scaled)

    def _exit_fullscreen(self) -> None:
        if self._fullscreen_window is not None:
            self._fullscreen_window.close()
        self._fullscreen_window = None
        self._fullscreen_label = None

    def _connect_worker(self) -> None:
        self._signals.connect_enabled.emit(False)
        self._signals.disconnect_enabled.emit(False)
        try:
            self._signals.status_changed.emit("Recherche de caméra sur le réseau...")
            preferred_ip = str(getattr(self.config.network, "camera_ip", "") or "")
            discovered = self.camera_service.discover_cameras(preferred_ip or None)

            selected_ip = None
            if preferred_ip and preferred_ip in discovered:
                selected_ip = preferred_ip
            elif discovered:
                selected_ip = discovered[0]
            elif preferred_ip:
                selected_ip = preferred_ip

            if not selected_ip:
                self._signals.status_changed.emit("Aucune caméra trouvée")
                return

            self.current_camera_ip = selected_ip
            self.config.network.camera_ip = selected_ip
            try:
                self.config.save()
            except Exception:
                logger.exception("Failed to persist selected camera IP")

            self._signals.status_changed.emit(f"Caméra détectée: {selected_ip}")
            self._start_stream(selected_ip)

        except Exception as exc:
            logger.exception("Camera discovery/connection failed")
            self._signals.status_changed.emit(f"Erreur connexion caméra: {exc}")
            self._signals.disconnect_enabled.emit(False)
        finally:
            self._signals.connect_enabled.emit(True)

    def _start_stream(self, ip: str) -> None:
        self.stop_stream()
        self.current_camera_ip = ip
        self._stream_stop.clear()
        self._stream_thread = threading.Thread(target=self._stream_worker, args=(ip,), daemon=True)
        self._stream_thread.start()

    def _stream_worker(self, ip: str) -> None:
        cap = None
        try:
            self._signals.status_changed.emit(f"Connexion au flux RTSP ({ip})...")
            stream_url = self.camera_service.find_working_rtsp_url(ip)
            if not stream_url:
                self._signals.status_changed.emit(f"Flux RTSP introuvable pour {ip}")
                return

            cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

            if not cap.isOpened():
                self._signals.status_changed.emit(f"Impossible d'ouvrir le flux vidéo {ip}")
                self._signals.disconnect_enabled.emit(False)
                return

            self._signals.status_changed.emit(f"Flux actif: {ip}")
            self._signals.disconnect_enabled.emit(True)
            read_failures = 0
            while not self._stream_stop.is_set():
                ok, frame = cap.read()
                if not ok or frame is None:
                    read_failures += 1
                    if read_failures > 50:
                        self._signals.status_changed.emit("Perte du flux vidéo")
                        self._signals.disconnect_enabled.emit(False)
                        break
                    continue

                read_failures = 0
                self._signals.frame_ready.emit(frame)

        except Exception as exc:
            logger.exception("Camera stream worker failed")
            self._signals.status_changed.emit(f"Erreur flux caméra: {exc}")
            self._signals.disconnect_enabled.emit(False)
        finally:
            if cap is not None:
                cap.release()

    def stop_stream(self) -> None:
        self._stream_stop.set()
        if self._stream_thread and self._stream_thread.is_alive():
            self._stream_thread.join(timeout=1.0)
        self._stream_thread = None
        self.current_camera_ip = None
        self._last_pixmap = None
        self._signals.disconnect_enabled.emit(False)

    def _on_status_changed(self, message: str) -> None:
        label = self._video_label
        if label is not None and not label.pixmap():
            label.setText(message)

        if hasattr(self.main_window, "set_log_text"):
            self.main_window.set_log_text(message)

    def _set_connect_button_enabled(self, enabled: bool) -> None:
        button = getattr(self.ui, "connect_cam_button", None)
        if button is not None:
            button.setEnabled(enabled)

    def _set_disconnect_button_enabled(self, enabled: bool) -> None:
        button = getattr(self.ui, "disconnect_cam_button", None)
        if button is not None:
            button.setEnabled(enabled)

    def _on_frame_ready(self, frame: np.ndarray) -> None:
        label = self._video_label
        if label is None or frame is None or frame.size == 0:
            return

        try:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channels = rgb.shape
            bytes_per_line = channels * width
            image = QImage(rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)

            base_pixmap = QPixmap.fromImage(image)
            pixmap = base_pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(pixmap)
            self._last_pixmap = base_pixmap
            self._set_fullscreen_pixmap(base_pixmap)
        except Exception:
            logger.exception("Failed to render camera frame")
