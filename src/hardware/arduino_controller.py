#!/usr/bin/env python3
# coding: utf-8

"""Arduino controller helper.

This module provides a robust, testable `ArduinoController` class that:
- loads configuration via `Config.load_default()` or accepts an injected config
- manages a background thread that reads analog pins periodically
- writes measurements to a CSV file safely (thread lock + file header handling)
- attempts reconnection on failures

Notes:
- Uses `nanpy` if available; otherwise still operates but no physical reads.
"""

from __future__ import annotations

import csv
import logging
import os
import threading
import time
from pathlib import Path
from typing import Dict, Optional

try:
    from nanpy import ArduinoApi, SerialManager
    _HAS_NANPY = True
except Exception:
    ArduinoApi = None
    SerialManager = None
    _HAS_NANPY = False

from ..config.manager import Config

logger = logging.getLogger(__name__)


class ArduinoController:
    """Manage Arduino connection and periodic current measurements.

    Usage:
        ctrl = ArduinoController(config=Config.load_default())
        ctrl.init_csv()
        ctrl.start_record()
        ... ctrl.stop_record()
    """

    DEFAULT_INTERVAL = 1.0  # seconds between readings
    FIELDNAMES = ["neutre", "phase1", "phase2", "phase3", "time"]

    def __init__(self, config: Optional[Config] = None, interval: float | None = None):
        self.config = config or Config.load_default()
        self.interval = float(interval) if interval is not None else self.DEFAULT_INTERVAL

        # Paths
        paths_cfg = getattr(self.config, "paths", None)
        hardware_cfg = getattr(self.config, "hardware", None)
        self.data_file = Path(
            getattr(paths_cfg, "data_file", getattr(self.config, "data_file", "data/measurements.csv"))
        )
        self.arduino_port = str(
            getattr(hardware_cfg, "arduino_port", getattr(self.config, "arduino_port", "/dev/ttyACM0"))
        )

        # State
        self._serial = None
        self._arduino = None
        self.connected = False

        # Threading
        self._lock = threading.Lock()
        self._running = threading.Event()
        self._thread: Optional[threading.Thread] = None

        # Last read values
        self._last_values: Dict[str, float | str] = {k: 0 for k in self.FIELDNAMES}
        # Try to connect now (non-fatal)
        if _HAS_NANPY:
            try:
                self._connect()
            except Exception:
                logger.debug("Initial Arduino connection failed, will retry on reads")
        else:
            logger.warning("nanpy not available — Arduino reads will be mocked")

    # ----- Connection handling -----
    def _connect(self) -> None:
        """Establish a SerialManager and ArduinoApi connection."""
        if not _HAS_NANPY:
            raise RuntimeError("nanpy is not available")

        if self._serial:
            try:
                self._serial.close()
            except Exception as e:
                logger.debug("Failed to close previous serial connection: %s", e)

        self._serial = SerialManager(device=self.arduino_port, timeout=2)
        self._arduino = ArduinoApi(connection=self._serial)
        self.connected = True
        logger.info("Arduino connected on %s", self.arduino_port)

    def _disconnect(self) -> None:
        try:
            if self._serial:
                self._serial.close()
        except Exception as e:
            logger.debug("Error closing serial during disconnect: %s", e)
        self._serial = None
        self._arduino = None
        self.connected = False
        logger.info("Arduino disconnected")

    def reconnect(self, attempts: int = 3, delay: float = 1.0) -> bool:
        """Try to reconnect several times; return True on success."""
        for i in range(attempts):
            try:
                self._connect()
                return True
            except Exception as e:
                logger.debug("Reconnect attempt %d failed: %s", i + 1, e)
                time.sleep(delay)
        self.connected = False
        return False

    # ----- CSV helpers -----
    def init_csv(self) -> None:
        """Ensure CSV file exists and has a header."""
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.data_file.exists():
            with self._lock, open(self.data_file, "w", newline="") as fh:
                writer = csv.DictWriter(fh, fieldnames=self.FIELDNAMES)
                writer.writeheader()
            logger.info("Created CSV file: %s", self.data_file)

    def _write_header_if_missing(self) -> None:
        if not self.data_file.exists():
            self.init_csv()
            return
        # check first line
        try:
            with open(self.data_file, "r", newline="") as fh:
                first = fh.readline()
                if not first or all(h not in first for h in self.FIELDNAMES):
                    # rewrite header + existing content
                    with self._lock:
                        lines = fh.read()
                        with open(self.data_file, "w", newline="") as fh2:
                            writer = csv.DictWriter(fh2, fieldnames=self.FIELDNAMES)
                            writer.writeheader()
                            if lines:
                                fh2.write(lines)
        except Exception:
            # If anything goes wrong, ensure file exists with header
            self.init_csv()

    # ----- Reading / conversion -----
    @staticmethod
    def _analog_to_current(analog_value: int) -> float:
        """Convert raw analog reading (0-1023) to current (Amps).

        Formula preserved from original: value = (analog*5)/1024 ; current = (value*500)/5
        which simplifies to analog * 500 / 1024.
        """
        try:
            current = (analog_value * 500.0) / 1024.0
            return round(current, 2)
        except Exception:
            return 0.0

    def _read_pin(self, pin: int) -> float:
        if not _HAS_NANPY or not self.connected or self._arduino is None:
            # Return 0.0 when hardware isn't available
            raise RuntimeError("Arduino not connected")
        raw = int(self._arduino.analogRead(int(pin)))
        return self._analog_to_current(raw)

    def read_values(self) -> Dict[str, float | str]:
        """Read all configured pins and return a dict of values.

        Raises RuntimeError if read fails.
        """
        try:
            vals = {
                "neutre": self._read_pin(0),
                "phase1": self._read_pin(1),
                "phase2": self._read_pin(2),
                "phase3": self._read_pin(3),
                "time": time.strftime("%H:%M:%S"),
            }
            self._last_values = vals
            return vals
        except Exception:
            raise

    # ----- CSV write -----
    def write_to_csv(self, data: Optional[Dict[str, float | str]] = None) -> None:
        data = data or self._last_values
        self._write_header_if_missing()
        with self._lock, open(self.data_file, "a", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=self.FIELDNAMES)
            writer.writerow({k: data.get(k, 0) for k in self.FIELDNAMES})

    # ----- Thread control -----
    def start_record(self) -> None:
        """Start background thread that reads and appends measurements periodically."""
        if self._thread and self._thread.is_alive():
            logger.debug("Record thread already running")
            return

        self._running.set()
        self._thread = threading.Thread(target=self._record_loop, name="ArduinoReadThread", daemon=True)
        self._thread.start()
        logger.info("Started Arduino recording thread")

    def _record_loop(self) -> None:
        while self._running.is_set():
            try:
                if not self.connected:
                    self.reconnect(attempts=2, delay=1.0)

                try:
                    values = self.read_values()
                except RuntimeError:
                    # If read failed due to connection, write zeros and continue
                    values = {k: 0 for k in self.FIELDNAMES}
                    values["time"] = time.strftime("%H:%M:%S")

                self.write_to_csv(values)
                time.sleep(self.interval)
            except Exception as e:
                logger.exception("Unhandled error in Arduino record loop: %s", e)
                # short sleep to avoid busy loop on unexpected errors
                time.sleep(1.0)

    def stop_record(self, join_timeout: float = 1.0) -> None:
        """Stop the background reading thread and disconnect the Arduino."""
        self._running.clear()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=join_timeout)
        try:
            self._disconnect()
        except Exception as e:
            logger.exception("Error during stop_record disconnect: %s", e)
        logger.info("Stopped Arduino recording")

    # ----- Utilities -----
    def get_latest_values(self) -> Dict[str, float | str]:
        """Return the last read measurement (may be zeros if no read yet)."""
        return dict(self._last_values)


__all__ = ["ArduinoController"]
