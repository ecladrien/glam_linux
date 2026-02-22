from __future__ import annotations
from pydantic import BaseModel, Field, model_validator
import os
import logging
from typing import List, Optional
from pathlib import Path
import json


# Resolve project root (two levels up from src/config)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
PATHCONFIG = PROJECT_ROOT / "data" / "config.json"

logger = logging.getLogger(__name__)

class DisplayConfig(BaseModel):
    screen_width: int = 1920
    screen_height: int = 1080
    fullscreen: bool = False

class HardwareConfig(BaseModel):
    arduino_port: str = "/dev/ttyACM0" #"/dev/cu.usbmodem1101"

class NetworkConfig(BaseModel):
    camera_ip: str = "192.168.1.188"
    device_ip: str = "192.168.1.69"
    artnet_network: str = "2.0.0.69"

class PathsConfig(BaseModel):
    data_file: Path = PROJECT_ROOT / "data" / "measurements.csv"
    plan_dir: Path = PROJECT_ROOT / "ressources" / "plans"
    default_img: Path = PROJECT_ROOT / "ressources" / "img" / "unicorn.png"
    head_img: Path = PROJECT_ROOT / "ressources" / "img" / "unicorn.png"
    
class CameraConfig(BaseModel):
    rtsp_stream: str = "/h264Preview_01_main"
    onvif_port: int = 8000
    rtsp_user: str = "admin"
    rtsp_password: str = Field(default_factory=lambda: os.getenv("RTSP_PASSWORD", ""))

class QlcConfig(BaseModel):
    qlc_folder_path: Path = Path("./ressources/qlc_files")
    qlc_file_path: Path = Path("./ressources/qlc_files/default.qxw")


class Config(BaseModel):
    display: DisplayConfig = Field(default_factory=DisplayConfig)
    hardware: HardwareConfig = Field(default_factory=HardwareConfig)
    network: NetworkConfig = Field(default_factory=NetworkConfig)
    qlc: QlcConfig = Field(default_factory=QlcConfig)
    paths: PathsConfig = Field(default_factory=PathsConfig)
    camera: CameraConfig = Field(default_factory=CameraConfig)

    @model_validator(mode="before")
    def _normalize_input(cls, values: dict):
        """Normalize legacy / convenience kwargs to nested structure.

        Allows calls like `Config(screen_width=800, screen_height=600)` or
        `Config(default_img="...", head_img="...")` by moving those keys
        into the appropriate nested sub-dicts (`display`, `paths`).
        """
        # Normalize display simple keys
        display = dict(values.get("display", {})) if isinstance(values, dict) else {}
        if "screen_width" in values:
            display["screen_width"] = values.pop("screen_width")
        if "screen_height" in values:
            display["screen_height"] = values.pop("screen_height")
        values["display"] = display

        # Normalize paths simple keys
        paths = dict(values.get("paths", {})) if isinstance(values, dict) else {}
        if "default_img" in values:
            paths["default_img"] = values.pop("default_img")
        if "head_img" in values:
            paths["head_img"] = values.pop("head_img")
        values["paths"] = paths

        return values

    @staticmethod
    def _normalize_project_path(path_value: Path | str) -> Path:
        p = Path(path_value)

        # Keep valid absolute external paths as-is.
        if p.is_absolute() and p.exists():
            return p

        # Fix malformed absolute values like "/ressources/..." or "/data/..."
        if p.is_absolute():
            try:
                rel = p.relative_to(Path("/"))
            except Exception:
                return p

            if rel.parts and rel.parts[0] in {"ressources", "data", "logs"}:
                return PROJECT_ROOT / rel

            return p

        # Relative paths are resolved against project root for deterministic behavior.
        return PROJECT_ROOT / p

    @staticmethod
    def _to_project_relative(path_value: Path | str) -> str:
        p = Path(path_value)
        try:
            return str(p.relative_to(PROJECT_ROOT))
        except Exception:
            return str(p)

    @model_validator(mode="after")
    def _normalize_paths(self) -> "Config":
        self.paths.data_file = self._normalize_project_path(self.paths.data_file)
        self.paths.plan_dir = self._normalize_project_path(self.paths.plan_dir)
        self.paths.default_img = self._normalize_project_path(self.paths.default_img)
        self.paths.head_img = self._normalize_project_path(self.paths.head_img)
        self.qlc.qlc_folder_path = self._normalize_project_path(self.qlc.qlc_folder_path)
        self.qlc.qlc_file_path = self._normalize_project_path(self.qlc.qlc_file_path)
        return self

    # Convenience properties for backward-compatibility with older callers/tests
    @property
    def screen_width(self) -> int:
        return int(self.display.screen_width)

    @property
    def screen_height(self) -> int:
        return int(self.display.screen_height)

    @property
    def default_img(self):
        return self.paths.default_img

    @property
    def head_img(self):
        return self.paths.head_img

    @classmethod
    def load_default(cls, path: Optional[str] = None) -> "Config":
        """Load config from file if exists, else return defaults."""
        if path is None:
            path_obj = Path(PATHCONFIG)
        else:
            path_obj = Path(path)
        try:
            if path_obj.exists():
                data = json.loads(path_obj.read_text())
                cfg = cls(**data)
                # Allow overriding secret via environment variable
                env_pw = os.getenv("RTSP_PASSWORD")
                if env_pw:
                    cfg.camera.rtsp_password = env_pw
                return cfg
        except Exception:
            logger.exception("Failed to load config from %s; falling back to defaults", path_obj)

        cfg = cls()
        env_pw = os.getenv("RTSP_PASSWORD")
        if env_pw:
            cfg.camera.rtsp_password = env_pw
        return cfg

    def save(self, path: Optional[str] = None) -> None:
        if path is None:
            path_obj = Path(PATHCONFIG)
            path_obj.parent.mkdir(parents=True, exist_ok=True)
        else:
            path_obj = Path(path)
        # Do not write secrets to disk; exclude password field when saving
        payload = self.model_dump(mode="json", exclude={"camera": {"rtsp_password"}})

        for section, keys in {
            "paths": ("data_file", "plan_dir", "default_img", "head_img"),
            "qlc": ("qlc_folder_path", "qlc_file_path"),
        }.items():
            block = payload.get(section, {})
            for key in keys:
                if key in block:
                    block[key] = self._to_project_relative(block[key])

        path_obj.write_text(json.dumps(payload, indent=4))
