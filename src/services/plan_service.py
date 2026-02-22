from __future__ import annotations
from pathlib import Path
from typing import List

from ..config.manager import Config


class PlanService:
    """Service de gestion des plans (découverte des fichiers et utilitaires).

    Cette couche contient la logique métier liée aux plans (où se trouvent
    les fichiers, quels formats sont acceptés, etc.). Elle ne dépend pas de
    l'UI.
    """

    IMAGE_EXT = {".jpg", ".jpeg", ".png", ".bmp", ".gif"}
    PDF_EXT = {".pdf"}

    def __init__(self, config: Config):
        self.config = config

    def get_plan_dir(self) -> Path:
        plan_dir = Path(getattr(self.config.paths, 'plan_dir', Path("./ressources/plans")))

        plan_dir.mkdir(parents=True, exist_ok=True)
        return plan_dir

    def list_plan_files(self) -> List[Path]:
        plan_dir = self.get_plan_dir()
        files: List[Path] = []
        try:
            for p in sorted(plan_dir.iterdir()):
                if not p.is_file():
                    continue
                if p.suffix.lower() in self.IMAGE_EXT.union(self.PDF_EXT):
                    files.append(p)
        except Exception:
            files = []

        return files

    def is_image(self, path: Path) -> bool:
        return path.suffix.lower() in self.IMAGE_EXT

    def is_pdf(self, path: Path) -> bool:
        return path.suffix.lower() in self.PDF_EXT
