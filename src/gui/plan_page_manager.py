from __future__ import annotations
from ..config.manager import Config
from pathlib import Path
from typing import List

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QGridLayout,
)
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QScrollArea, QDialog
from PySide6.QtCore import QSize

from ..services.plan_service import PlanService


class ClickableLabel(QLabel):
    clicked = Signal()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.clicked.emit()


class PlanPageManager:
    """Gère l'affichage des plans (images + pdf) dans la page 'plan_page'.
    """

    IMAGE_EXT = {".jpg", ".jpeg", ".png", ".bmp", ".gif"}
    PDF_EXT = {".pdf"}
    SCALE_FACTOR = 1.3  # Factor to reduce image size for thumbnails

    def __init__(self, main_window, config: Config):
        self.main_window = main_window
        self.config = config
        self.plan_service = PlanService(config)
        self.ui = main_window.ui
        self._current_fullscreen = None
 
        try:
            # Prepare the scroll area that will contain thumbnails
            self._prepare_ui()
            # Load files from configured plan directory
            self._load_plan_files()
        except Exception as e:
            if hasattr(self.main_window, 'set_log_text'):
                self.main_window.set_log_text(f"Erreur plan_page initialisation: {e}")

    def _prepare_ui(self) -> None:
        # Create a scrollable widget to hold thumbnails in a grid
        self.scroll = QScrollArea(self.ui.plan_page)
        self.scroll.setWidgetResizable(True)

        self.container = QWidget()
        self.grid = QGridLayout(self.container)
        self.grid.setContentsMargins(20, 20, 20, 20)
        self.grid.setSpacing(8)

        self.scroll.setWidget(self.container)

        # Add to the existing layout of the plan_page (horizontalLayout_4)
        try:
            self.ui.horizontalLayout_4.addWidget(self.scroll)
        except Exception:
            # fallback: if attribute missing, try to set as only child
            layout = QVBoxLayout(self.ui.plan_page)
            layout.addWidget(self.scroll)

    def _load_plan_files(self) -> None:
        # Delegate plan file discovery to the PlanService
        files: List[Path] = []
        try:
            files = self.plan_service.list_plan_files()
        except Exception:
            files = []

        # Clear existing grid
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()

        # Populate grid with thumbnails / pdf icons
        col = 0
        row = 0
        max_cols = 3
        for f in files:
            if f.suffix.lower() in self.IMAGE_EXT:
                lbl = ClickableLabel()
                pix = QPixmap(str(f))
                if not pix.isNull():

                    thumb = pix.scaled(self.ui.plan_page.width() // self.SCALE_FACTOR, self.ui.plan_page.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    lbl.setPixmap(thumb)
                else:
                    lbl.setText(f.name)
                lbl.setToolTip(str(f))
                lbl.file_path = f
                lbl.setCursor(Qt.PointingHandCursor)
                lbl.clicked.connect(lambda fp=f: self._on_image_clicked(fp))
                self.grid.addWidget(lbl, row, col)
            else:
                # PDF: show a clickable button that opens in default app
                btn = QPushButton(f.name)
                btn.setCursor(Qt.PointingHandCursor)
                btn.clicked.connect(lambda checked=False, fp=f: self._open_file_with_default(fp))
                self.grid.addWidget(btn, row, col)

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    def refresh_plans(self) -> None:
        """Reload plan files and refresh the UI (public method).

        Call this after external changes to the `plan_dir` so the page updates.
        """
        try:
            self._load_plan_files()
        except Exception as e:
            if hasattr(self.main_window, 'set_log_text'):
                self.main_window.set_log_text(f"Erreur lors du rafraîchissement des plans: {e}")

    def _open_file_with_default(self, path: Path) -> None:
        try:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))
        except Exception as e:
            if hasattr(self.main_window, 'set_log_text'):
                self.main_window.set_log_text(f"Impossible d'ouvrir {path}: {e}")

    def _on_image_clicked(self, path: Path) -> None:
        try:
            if self._current_fullscreen and self._current_fullscreen.isVisible():
                # If already showing same image, close it
                self._current_fullscreen.close()
                self._current_fullscreen = None
                return

            pix = QPixmap(str(path))
            if pix.isNull():
                if hasattr(self.main_window, 'set_log_text'):
                    self.main_window.set_log_text(f"Impossible de charger l'image: {path}")
                return

            dlg = FullscreenImageDialog(pix, parent=self.main_window)
            self._current_fullscreen = dlg
            dlg.showFullScreen()
        except Exception as e:
            if hasattr(self.main_window, 'set_log_text'):
                self.main_window.set_log_text(f"Erreur affichage image: {e}")


class FullscreenImageDialog(QDialog):
    def __init__(self, pixmap: QPixmap, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.Window)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self._pix = pixmap
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        self._update_pixmap()

    def _update_pixmap(self):
        screen = self.screen() or None
        if screen is not None:
            size = screen.availableGeometry().size()
        else:
            size = QSize(1920, 1080)
        scaled = self._pix.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(scaled)

    def mousePressEvent(self, event):
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)
    
