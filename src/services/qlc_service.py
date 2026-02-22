from __future__ import annotations
from pathlib import Path
from typing import Optional
import shutil
import subprocess
import logging

from ..config.manager import Config, QlcConfig


class QlcService:
    """Service pour la gestion des fichiers QLC+ et lancement de l'application.

    Fournit la logique métier indépendante de l'UI : résolution du fichier
    courant, dossier de démarrage pour le dialogue, persistance du choix,
    recherche de l'exécutable et lancement.
    """

    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def get_default_file(self) -> Path:
        return QlcConfig().qlc_file_path

    def resolve_current_file(self) -> Path:
        fp = getattr(self.config.qlc, 'qlc_file_path', None)
        default_file = self.get_default_file()

        if fp:
            p = Path(fp)

            if not p.exists():
                try:
                    self.config.qlc.qlc_file_path = default_file
                    self.config.save()
                    self.logger.debug('Reset qlc_file_path to default because stored file was missing')
                except Exception:
                    self.logger.exception('Failed to reset qlc_file_path to default')
                return default_file

            return p

        return default_file

    def choose_start_dir(self) -> Path:
        start_dir = Path(getattr(self.config.qlc, 'qlc_folder_path', Path('./')))
        return start_dir

    def set_chosen_file(self, path: Path) -> None:
        try:
            self.config.qlc.qlc_folder_path = path.parent
            self.config.qlc.qlc_file_path = path
            self.config.save()
        except Exception:
            self.logger.exception('Failed to update config with chosen qlc file')

    def find_qlc_executable(self) -> Optional[Path]:
        exe = Path('/usr/bin/qlcplus')
        if exe.exists():
            return exe
        found = shutil.which('qlcplus')
        if found:
            return Path(found)
        return None

    def launch_qlc(self, path: Path) -> bool:
        exe = self.find_qlc_executable()
        if not exe:
            return False
        cmd = [str(exe), '--operate', '--overscan', '--open', str(path)]
        try:
            subprocess.Popen(cmd)
            self.logger.debug('Launched qlcplus: %s', cmd)
            return True
        except Exception:
            self.logger.exception('Failed to launch qlcplus')
            return False
