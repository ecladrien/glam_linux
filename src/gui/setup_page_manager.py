from ..config.manager import Config
from PySide6.QtWidgets import QLineEdit, QPushButton, QFileDialog, QMessageBox
from pathlib import Path
import logging

from ..services.setup_service import SetupService

logger = logging.getLogger(__name__)


class SetupPageManager:
    def __init__(self, main_window, config: Config):
        self.main_window = main_window
        self.config = config
        self.ui = main_window.ui
        self.setup_service = SetupService(config)
        self._connect_buttons()
        self.load_config_to_fields()

    def load_config_to_fields(self):
        try:
            vals = self.setup_service.get_config_values()
            self.ui.width_screen_line_edit.setText(str(vals.get('screen_width', '')))
            self.ui.height_screen_line_edit.setText(str(vals.get('screen_height', '')))
            self.ui.adress_ip_line_edit.setText(str(vals.get('device_ip', '')))
            self.ui.adress_ip_cam_line_edit.setText(str(vals.get('camera_ip', '')))
            self.ui.adress_ip_artnet_line_edit.setText(str(vals.get('artnet_network', '')))
            self.ui.port_cam_line_edit.setText(str(vals.get('onvif_port', '')))
            self.ui.user_cam_line_edit.setText(str(vals.get('rtsp_user', '')))
            self.ui.password_cam_line_edit.setText(str(vals.get('rtsp_password', '')))
        except Exception as e:
            logger.exception("Erreur lors du chargement de la configuration: %s", e)

    def save_fields_to_config(self):
        try:
            values = {
                'screen_width': int(self.ui.width_screen_line_edit.text()),
                'screen_height': int(self.ui.height_screen_line_edit.text()),
                'device_ip': self.ui.adress_ip_line_edit.text(),
                'camera_ip': self.ui.adress_ip_cam_line_edit.text(),
                'artnet_network': self.ui.adress_ip_artnet_line_edit.text(),
                'onvif_port': int(self.ui.port_cam_line_edit.text()),
                'rtsp_user': self.ui.user_cam_line_edit.text(),
                'rtsp_password': self.ui.password_cam_line_edit.text(),
            }
            reply = QMessageBox.question(
                self.main_window,
                "Confirmer sauvegarde",
                "Sauvegarder les modifications apportées à la configuration ?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if reply != QMessageBox.Yes:
                return

            self.setup_service.save_config_values(values)
            if hasattr(self.main_window, 'set_log_text'):
                self.main_window.set_log_text('Configuration sauvegardée.')
        except Exception as e:
            if hasattr(self.main_window, 'set_log_text'):
                self.main_window.set_log_text(f'Erreur lors de la sauvegarde: {e}')
            logger.exception("Erreur lors de la sauvegarde de la configuration: %s", e)

    def reset_to_default(self):
        # Demander confirmation avant de réinitialiser les champs (non sauvegardés)
        try:
            reply = QMessageBox.question(
                self.main_window,
                "Confirmer restauration",
                "Restaurer les valeurs par défaut (les changements actuels ne seront pas sauvegardés) ?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if reply != QMessageBox.Yes:
                return
        except Exception:
            # Si la boîte de dialogue échoue, continuer sans confirmer
            self.main_window.set_log_text("Impossible d'afficher la boîte de confirmation, restauration par défaut annulée.")

        self.setup_service.reset_to_defaults()
        self.load_config_to_fields()
        if hasattr(self.main_window, 'set_log_text'):
            self.main_window.set_log_text('Valeurs par défaut restaurées (non sauvegardées).')

    def _connect_buttons(self):
        self.ui.save_setup_button.clicked.connect(self.save_fields_to_config)
        self.ui.reset_setup_button.clicked.connect(self.reset_to_default)
        # Choix d'image d'arrière-plan (head image)
        try:
            self.ui.background_img_choose_button.clicked.connect(self._background_img_choose_button_clicked)
        except Exception as e:
            logger.debug("background_img_choose_button not available or not connectable: %s", e)
        # Charger des plans (images / PDF) dans ressources/plans
        try:
            self.ui.plan_charge_button.clicked.connect(self._plan_charge_button_clicked)
        except Exception as e:
            logger.debug("plan_charge_button not available or not connectable: %s", e)
        # Supprimer des plans de ressources/plans
        try:
            self.ui.plan_delete_button.clicked.connect(self._plan_delete_button_clicked)
        except Exception as e:
            logger.debug("plan_delete_button not available or not connectable: %s", e)

    def _plan_charge_button_clicked(self):
        try:
            files, _ = QFileDialog.getOpenFileNames(
                self.main_window,
                "Ajouter des plans (images ou PDF)",
                str(Path(".")),
                "Plans (*.png *.jpg *.jpeg *.bmp *.pdf);;Tout (*.*)",
                options=QFileDialog.Option.DontUseNativeDialog,
            )
            if not files:
                return

            result = self.setup_service.add_plans([Path(f) for f in files])
            msg = f"{result.get('count_copied', 0)} fichier(s) copiés dans {result.get('target_dir')}"
            logger.info(msg)
            if hasattr(self.main_window, 'set_log_text'):
                self.main_window.set_log_text(msg)
            # Demander au gestionnaire de page des plans de se rafraîchir
            if hasattr(self.main_window, 'plan_page_manager') and hasattr(self.main_window.plan_page_manager, 'refresh_plans'):
                try:
                    self.main_window.plan_page_manager.refresh_plans()
                except Exception:
                    logger.exception("Erreur rafraîchissement plan_page_manager après ajout")
        except Exception as e:
            logger.exception("Erreur lors du chargement des plans: %s", e)
            if hasattr(self.main_window, 'set_log_text'):
                self.main_window.set_log_text(f'Erreur lors du chargement des plans: {e}')

    def _plan_delete_button_clicked(self):
        try:
            target_dir = self.config.paths.plan_dir
            target_dir.mkdir(parents=True, exist_ok=True)

            files, _ = QFileDialog.getOpenFileNames(
                self.main_window,
                "Sélectionner les plans à supprimer",
                str(target_dir),
                "Plans (*.png *.jpg *.jpeg *.bmp *.pdf);;Tout (*.*)",
                options=QFileDialog.Option.DontUseNativeDialog,
            )
            if not files:
                return

            # Confirmation
            count = len(files)
            reply = QMessageBox.question(
                self.main_window,
                "Confirmer suppression",
                f"Supprimer {count} fichier(s) de {target_dir}?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if reply != QMessageBox.Yes:
                return

            result = self.setup_service.delete_plans([Path(f) for f in files])
            msg = f"{result.get('deleted', 0)}/{result.get('total', 0)} fichier(s) supprimés de {result.get('target_dir')}"
            logger.info(msg)
            if hasattr(self.main_window, 'set_log_text'):
                self.main_window.set_log_text(msg)
            # Rafraîchir la page des plans si présente
            if hasattr(self.main_window, 'plan_page_manager') and hasattr(self.main_window.plan_page_manager, 'refresh_plans'):
                try:
                    self.main_window.plan_page_manager.refresh_plans()
                except Exception:
                    logger.exception("Erreur rafraîchissement plan_page_manager après suppression")

        except Exception as e:
            logger.exception("Erreur lors de la suppression des plans: %s", e)
            if hasattr(self.main_window, 'set_log_text'):
                self.main_window.set_log_text(f'Erreur lors de la suppression des plans: {e}')

    def _background_img_choose_button_clicked(self):
        try:
            fname, _ = QFileDialog.getOpenFileName(
                self.main_window,
                "Choisir une image de fond",
                str(Path(".")),
                "Images (*.png *.jpg *.jpeg *.bmp)",
                options=QFileDialog.Option.DontUseNativeDialog,
            )
            if not fname:
                return

            # Mettre à jour via le service
            self.setup_service.set_head_image(Path(fname))

            # Si la page d'accueil est présente, demander le rafraîchissement
            if hasattr(self.main_window, 'home_page_manager') and hasattr(self.main_window.home_page_manager, 'set_head_image'):
                try:
                    self.main_window.home_page_manager.set_head_image(Path(fname))
                except Exception:
                    # Ne pas laisser planter l'UI principale
                    logger.exception("Erreur lors du rafraîchissement du background de la home page")
            else:
                if hasattr(self.main_window, 'set_log_text'):
                    self.main_window.set_log_text('Image de fond sélectionnée et sauvegardée.')
        except Exception as e:
            logger.exception("Erreur sélection image de fond: %s", e)
            if hasattr(self.main_window, 'set_log_text'):
                self.main_window.set_log_text(f'Erreur sélection image de fond: {e}')
