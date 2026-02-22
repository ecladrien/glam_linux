from ..config.manager import Config
from pathlib import Path
from PySide6.QtCore import Qt, QTimer, QDateTime
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMainWindow
from .home_page_manager import HomePageManager
from .plan_page_manager import PlanPageManager
from .qlc_page_manager import QlcPageManager
from .cam_page_manager import CamPageManager
from .setup_page_manager import SetupPageManager
from .measurement_page_management import MeasurementPageManager
from .Ui_MainWindow import Ui_MainWindow
import logging

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):

    """Fenêtre principale avec gestion des signaux et slots."""

    def __init__(self, config: Config | None = None, fullscreen: bool = False):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.config = config
        self.fullscreen_mode = fullscreen

        # Appliquer la taille de fenêtre depuis la config si disponible (ignorée si fullscreen)
        if config is not None and not fullscreen:
            try:
                if getattr(config.display, "screen_width", None) and getattr(config.display, "screen_height", None):
                    self.resize(int(config.display.screen_width), int(config.display.screen_height))
            except Exception:
                if hasattr(self, 'set_log_text'):
                    self.set_log_text("Erreur application taille fenêtre depuis config - vérifier les valeurs de screen_width et screen_height")

        # Connecter les boutons de la barre latérale aux pages correspondantes
        try:
            self.ui.home_button.clicked.connect(lambda: self.ui.main_frame.setCurrentWidget(self.ui.home_page))
            self.ui.plan_button.clicked.connect(lambda: self.ui.main_frame.setCurrentWidget(self.ui.plan_page))
            self.ui.measurement_button.clicked.connect(lambda: self.ui.main_frame.setCurrentWidget(self.ui.measurement_page))
            self.ui.cam_button.clicked.connect(lambda: self.ui.main_frame.setCurrentWidget(self.ui.cam_page))
            self.ui.qlc_button.clicked.connect(lambda: self.ui.main_frame.setCurrentWidget(self.ui.qlc_page))
            self.ui.setup_button.clicked.connect(lambda: self.ui.main_frame.setCurrentWidget(self.ui.setup_page))
        except Exception:
            if hasattr(self, 'set_log_text'):
                    self.set_log_text("Erreur connexion boutons de navigation - vérifier que les boutons et pages existent dans le .ui")


        # Charger l'image de la page d'accueil: `head_img` sinon `default_img`.
        try:
            self.cfg = self.config if self.config is not None else Config.load_default()
            self.head_path = Path(self.cfg.head_img)
            self.default_path = Path(self.cfg.default_img)
        except Exception:
            if hasattr(self, 'set_log_text'):
                    self.set_log_text("Erreur chargement paths.head_img/default_img depuis config - vérifier les valeurs dans la config")

        # Affichage de la date et l'heure dans le time label
        try:
            self._update_time_label()
            self._timer_time = QTimer(self)
            self._timer_time.timeout.connect(self._update_time_label)
            self._timer_time.start(1000)
        except Exception as e:
            if hasattr(self, 'set_log_text'):
                self.set_log_text(f"Erreur timer horloge: {e}")

        # Initialiser la gestion de la home_page
        try:
            self.home_page_manager = HomePageManager(self, self.cfg)
        except Exception as e:
            logger.exception("Erreur affichage home_page: %s", e)

        # Initialiser la gestion des plans (thumbnails et affichage plein écran)
        try:
            self.plan_page_manager = PlanPageManager(self, self.cfg)
        except Exception as e:
            logger.exception("Erreur affichage plan_page: %s", e)

        # Initialiser la gestion de la measurement_page
        try:
            self.measurement_page_manager = MeasurementPageManager(self, self.cfg)
        except Exception as e:
            logger.exception("Erreur affichage measurement_page: %s", e)

        # Initialiser la gestion de la cam_page (détecte et affiche les caméras)
        try:
            self.cam_page_manager = CamPageManager(self, self.cfg)
        except Exception as e:
            logger.exception("Erreur affichage cam_page: %s", e)

        # Initialiser la gestion de la qlc_page
        try:
            self.qlc_page_manager = QlcPageManager(self, self.cfg)
        except Exception as e:
            logger.exception("Erreur affichage qlc_page: %s", e)

        # Initialiser la gestion de la setup_page
        try:
            self.setup_page_manager = SetupPageManager(self, self.cfg)
        except Exception as e:
            logger.exception("Erreur affichage setup_page: %s", e)

    def closeEvent(self, event):
        try:
            if hasattr(self, "measurement_page_manager"):
                cleanup = getattr(self.measurement_page_manager, "_cleanup", None)
                if callable(cleanup):
                    cleanup()
        except Exception:
            logger.exception("Erreur fermeture measurement_page_manager")

        try:
            if hasattr(self, "cam_page_manager"):
                self.cam_page_manager.stop_stream()
        except Exception:
            logger.exception("Erreur arrêt cam_page_manager")

        super().closeEvent(event)
        
    def keyPressEvent(self, event):
        """Gérer les événements clavier - Échap pour basculer plein écran."""
        try:
            if event.key() == Qt.Key.Key_Escape:
                if self.isFullScreen():
                    self.showNormal()
                    if hasattr(self, 'set_log_text'):
                        self.set_log_text("Mode plein écran désactivé")
                else:
                    self.showFullScreen()
                    if hasattr(self, 'set_log_text'):
                        self.set_log_text("Mode plein écran activé")
                return
        except Exception as e:
            logger.exception("Erreur gestion touche Escape: %s", e)
        
        # Appeler la classe parente pour les autres touches
        super().keyPressEvent(event)
        
    def _update_time_label(self):
        try:
            now = QDateTime.currentDateTime()
            label = getattr(self.ui, "time_label", None)
            if label is not None:
                label.setText(now.toString("dd/MM/yyyy HH:mm:ss"))
        except Exception as e:
            logger.exception("Erreur affichage time_label: %s", e)


    def set_log_text(self, text: str) -> None:
        """Place le texte dans la zone de log de la barre de statut."""
        try:
            if hasattr(self.ui, "log") and self.ui.log is not None:
                self.ui.log.setText(str(text))
        except Exception as e:
            logger.exception("Erreur affichage log: %s", e)

