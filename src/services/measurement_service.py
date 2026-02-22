from __future__ import annotations
from pathlib import Path
import shutil
import csv
from typing import Optional

from ..config.manager import Config
from ..hardware.arduino_controller import ArduinoController


class MeasurementService:
    """Service pour la gestion du fichier de mesures (CSV).

    Fournit les opérations métiers sur le stockage des mesures :
    résolution du chemin, copie (export), et réinitialisation.
    """

    def __init__(self, config: Config):
        self.config = config

    def get_data_file(self) -> Path:
        try:
            data_file = Path(self.config.paths.data_file)
        except Exception:
            data_file = Path(getattr(self.config, 'data_file', Path('data/measurements.csv')))

        data_file.parent.mkdir(parents=True, exist_ok=True)
        return data_file

    def copy_to(self, src: Optional[Path], dest: Path) -> None:
        srcf = src or self.get_data_file()
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(srcf), str(dest))

    def reset_file(self, target: Optional[Path] = None) -> None:
        """Truncate le fichier de mesures et écrit l'en-tête CSV.

        Si `ArduinoController.FIELDNAMES` est disponible, l'utilise comme en-tête.
        """
        target_file = target or self.get_data_file()
        target_file.parent.mkdir(parents=True, exist_ok=True)
        header = getattr(ArduinoController, 'FIELDNAMES', None)
        with open(target_file, 'w', newline='') as fh:
            writer = csv.writer(fh)
            if header:
                writer.writerow(header)
            else:
                writer.writerow(['time'])
