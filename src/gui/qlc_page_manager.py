from __future__ import annotations
from ..config.manager import Config, QlcConfig
from pathlib import Path
import logging

from PySide6.QtWidgets import QFileDialog

from ..config.manager import QlcConfig
from ..services.qlc_service import QlcService

logger = logging.getLogger(__name__)


class QlcPageManager:
    def __init__(self, main_window, config: Config):
        self.main_window = main_window
        self.config = config
        self.ui = main_window.ui
        self.qlc_service = QlcService(config)

        # Ensure UI label shows current qlc file (or default) and validate existence
        try:
            chosen_path = self.qlc_service.resolve_current_file()
            try:
                self.ui.path_choose_qlc_file_label.setText(str(chosen_path))
            except Exception:
                logger.debug('Failed to set initial qlc file label text')
        except Exception:
            logger.debug('Error while validating initial qlc file')

        # Connect the choose button to open a file dialog for .qxw files
        try:
            def _choose_qlc_file() -> None:
                start_dir = self.qlc_service.choose_start_dir()

                file_path, _ = QFileDialog.getOpenFileName(self.main_window,
                                                           "Choisir un fichier QLC+ (.qxw)",
                                                           str(start_dir),
                                                           "QLC+ Project (*.qxw)",
                                                           options=QFileDialog.Option.DontUseNativeDialog)
                if file_path:
                    p = Path(file_path)
                    self.qlc_service.set_chosen_file(p)
                    try:
                        self.ui.path_choose_qlc_file_label.setText(str(p))
                    except Exception as e:
                        logger.debug('Failed to set qlc file label to chosen file: %s', e)
                else:
                    try:
                        self.ui.path_choose_qlc_file_label.setText(str(getattr(self.config.qlc, 'qlc_file_path', '')))
                    except Exception as e:
                        logger.debug('Failed to set qlc file label fallback: %s', e)

            try:
                self.ui.choose_qlc_file_button.clicked.connect(_choose_qlc_file)
            except Exception as e:
                logger.debug("choose_qlc_file_button not available to connect: %s", e)
        except Exception:
            logger.debug("PySide6 not available or QFileDialog import failed")

        # Connect the run button to start qlcplus with the chosen file
        try:
            def _run_qlc() -> None:
                path = self.qlc_service.resolve_current_file()
                if not path or not path.exists():
                    if hasattr(self.main_window, 'set_log_text'):
                        self.main_window.set_log_text(f'Fichier QLC introuvable: {path}')
                    logger.debug('QLC file does not exist: %s', path)
                    return

                exe = self.qlc_service.find_qlc_executable()
                if not exe:
                    if hasattr(self.main_window, 'set_log_text'):
                        self.main_window.set_log_text(f'Executable qlcplus introuvable')
                    logger.debug('qlcplus executable not found')
                    return

                try:
                    self.qlc_service.launch_qlc(path)
                except Exception as e:
                    logger.exception('Failed to launch qlcplus')
                    if hasattr(self.main_window, 'set_log_text'):
                        self.main_window.set_log_text(f'Erreur lancement qlcplus: {e}')

            try:
                self.ui.run_qlc_button.clicked.connect(_run_qlc)
            except Exception as e:
                logger.debug('run_qlc_button not available to connect: %s', e)
        except Exception:
            logger.debug('Failed to set up run_qlc_button handler')

