from __future__ import annotations
from pathlib import Path
from typing import Optional
import logging

from ..config.manager import Config

logger = logging.getLogger(__name__)


class HomeService:
    """Service fournissant la logique liée à la page d'accueil.

    - Résolution du chemin de l'image d'en-tête (head_img ou default)
    - Mise à jour du `head_img` et sauvegarde de la config
    - Exposition d'une méthode de sauvegarde de configuration
    """

    def __init__(self, config: Config):
        self.config = config

    def resolve_background_path(self) -> Optional[Path]:
        head_path = Path(getattr(self.config.paths, "head_img", ""))
        default_path = Path(getattr(self.config.paths, "default_img", ""))

        if head_path and head_path.exists():
            return head_path
        if default_path and default_path.exists():
            return default_path
        return None

    def set_head_image(self, path: Path) -> None:
        try:
            self.config.paths.head_img = Path(path)
            self.config.save()
        except Exception:
            logger.exception('Failed to set head image')
            raise

    def save_config(self) -> None:
        try:
            self.config.save()
        except Exception:
            logger.exception('Failed to save config')
            raise
