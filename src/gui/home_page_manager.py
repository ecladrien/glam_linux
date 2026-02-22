from ..config.manager import Config
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QProcess
from pathlib import Path
import sys
import os
from PySide6.QtGui import QPixmap
import logging

from ..services.home_service import HomeService

logger = logging.getLogger(__name__)


class HomePageManager:
    def __init__(self, main_window, config: Config):
        self.main_window = main_window
        self.config = config
        self.ui = main_window.ui
        self.home_service = HomeService(config)
        self._connect_buttons()
        # Afficher la home_page
        try:
            self.ui.main_frame.setCurrentWidget(self.ui.home_page)
            self._load_and_apply_background()
        except Exception as e:
            logger.exception("Erreur affichage home_page: %s", e)
            if hasattr(self.main_window, 'set_log_text'):
                self.main_window.set_log_text(f"Erreur affichage home_page: {e}")

    def _load_and_apply_background(self):
        try:
            chosen = self.home_service.resolve_background_path()

            if chosen is None:
                msg = "Aucune image de fond disponible (head_img ou default_img) - vérifier la config"
                logger.warning(msg)
                if hasattr(self.main_window, 'set_log_text'):
                    self.main_window.set_log_text(msg)
                return

            pix = QPixmap(str(chosen))
            if pix.isNull():
                msg = "Impossible de charger l'image de fond"
                logger.warning("%s: %s", msg, chosen)
                if hasattr(self.main_window, 'set_log_text'):
                    self.main_window.set_log_text(msg)
                return

            label = self.ui.background_image

            label.setScaledContents(False)
            w = max(1, (label.width()*2.5))
            h = max(1, (label.height()*2.5))
            scaled = pix.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(scaled)
        except Exception as e:
            logger.exception("Erreur application background: %s", e)
            if hasattr(self.main_window, 'set_log_text'):
                self.main_window.set_log_text(f"Erreur application background: {e}")

    def set_head_image(self, path: Path):
        """Met à jour `config.paths.head_img`, sauvegarde la config et rafraîchit l'affichage."""
        try:
            self.home_service.set_head_image(Path(path))
            self._load_and_apply_background()
        except Exception as e:
            logger.exception("Erreur lors de la mise à jour du head_img: %s", e)
            if hasattr(self.main_window, 'set_log_text'):
                self.main_window.set_log_text(f"Erreur lors de la mise à jour du head_img: {e}")


    def _connect_buttons(self):
        self.ui.restart_button.clicked.connect(self._restart_button_clicked)
        self.ui.shutdown_button.clicked.connect(self.shutdown_button_clicked)

    def _restart_button_clicked(self):
        # Sauvegarder la config si un gestionnaire est disponible, sinon sauvegarder la config brute
        self._save_config()

        # Redémarrer l'application
        try:
            logger.info("Redémarrage demandé via UI")
            QApplication.quit()
            QProcess.startDetached(sys.executable, sys.argv)
        except Exception as e:
            logger.exception("Erreur lors du redémarrage: %s", e)
            if hasattr(self.main_window, 'set_log_text'):
                self.main_window.set_log_text(f"Erreur lors du redémarrage: {e}")

    def shutdown_button_clicked(self):
        # Sauvegarder la config si possible
        self._save_config()

        # Tenter un arrêt propre si la plateforme le permet (peut nécessiter des privilèges)
        try:
            msg = 'Tentative d\'arrêt du système...'
            logger.info(msg)
            if hasattr(self.main_window, 'set_log_text'):
                self.main_window.set_log_text(msg)
            """
            if sys.platform.startswith("linux"):
                os.system("shutdown -h now")
            elif sys.platform == "darwin":
                # macOS shutdown via AppleScript (may prompt for privileges)
                os.system("osascript -e 'tell app \"System Events\" to shut down'")
            else:
                if hasattr(self.main_window, 'set_log_text'):
                    self.main_window.set_log_text('Shutdown non supporté sur ce système.')"""
        except Exception as e:
            logger.exception("Erreur shutdown: %s", e)
            if hasattr(self.main_window, 'set_log_text'):
                self.main_window.set_log_text(f'Erreur shutdown: {e}')


    def _save_config(self):
        try:
            if hasattr(self.main_window, 'setup_page_manager') and hasattr(self.main_window.setup_page_manager, 'save_fields_to_config'):
                self.main_window.setup_page_manager.save_fields_to_config()
            else:
                # delegate to service for saving
                self.home_service.save_config()
        except Exception as e:
            logger.exception("Erreur lors de la sauvegarde de la config: %s", e)
            if hasattr(self.main_window, 'set_log_text'):
                self.main_window.set_log_text(f"Erreur lors de la sauvegarde de la config: {e}")