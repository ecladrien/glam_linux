#!/usr/bin/env python3
# coding: utf-8

"""ESP32 serial controller helper.

This module keeps the historical `ArduinoController` public API so the rest of
the application does not need to change, but the transport is now a simple
serial protocol intended for an ESP32 WROOM firmware.

Expected protocol:
- host sends `PING\n`, device replies `PONG`
- host sends `READ\n`, device replies with one JSON line containing
    `neutre`, `phase1`, `phase2`, `phase3` and optionally `time`
"""

from __future__ import annotations

import csv
import json
import logging
import threading
import time
from pathlib import Path
from typing import Dict, Optional

try:
    import serial
    from serial import SerialException
    _HAS_SERIAL = True
except Exception:
    serial = None
    SerialException = Exception
    _HAS_SERIAL = False

from ..config.manager import Config

logger = logging.getLogger(__name__)


class ArduinoController:
    """Manage ESP32 connection and periodic current measurements.

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
        self.baudrate = int(
            getattr(hardware_cfg, "serial_baudrate", getattr(self.config, "serial_baudrate", 115200))
        )
        self.serial_timeout = float(
            getattr(hardware_cfg, "serial_timeout", getattr(self.config, "serial_timeout", 2.0))
        )
        self.boot_delay = float(
            getattr(hardware_cfg, "esp32_boot_delay", getattr(self.config, "esp32_boot_delay", 2.0))
        )

        # State
        self._serial = None
        self.connected = False

        # Threading
        self._file_lock = threading.Lock()
        self._serial_lock = threading.Lock()
        self._running = threading.Event()
        self._thread: Optional[threading.Thread] = None

        # Last read values
        self._last_values: Dict[str, float | str] = {k: 0 for k in self.FIELDNAMES}
        # Try to connect now (non-fatal)
        if _HAS_SERIAL:
            try:
                self._connect()
            except Exception:
                logger.debug("Initial ESP32 connection failed, will retry on reads")
        else:
            logger.warning("pyserial not available — ESP32 reads will be mocked")

    # ----- Connection handling -----
    def _connect(self) -> None:
        """Establish a serial connection to the ESP32 and validate the protocol."""
        if not _HAS_SERIAL:
            raise RuntimeError("pyserial is not available")

        if self._serial:
            try:
                self._serial.close()
            except Exception as e:
                logger.debug("Failed to close previous serial connection: %s", e)

        self._serial = serial.Serial(
            port=self.arduino_port,
            baudrate=self.baudrate,
            timeout=self.serial_timeout,
            write_timeout=self.serial_timeout,
        )
        time.sleep(self.boot_delay)
        self._reset_serial_buffers()
        reply = self._exchange_command("PING", expect_reply=True)
        if reply.strip().upper() != "PONG":
            self._serial.close()
            self._serial = None
            raise RuntimeError(f"Unexpected ESP32 handshake reply: {reply!r}")
        self.connected = True
        logger.info("ESP32 connected on %s", self.arduino_port)

    def _disconnect(self) -> None:
        try:
            if self._serial:
                self._serial.close()
        except Exception as e:
            logger.debug("Error closing serial during disconnect: %s", e)
        self._serial = None
        self.connected = False
        logger.info("ESP32 disconnected")

    def _reset_serial_buffers(self) -> None:
        if not self._serial:
            return
        try:
            self._serial.reset_input_buffer()
            self._serial.reset_output_buffer()
        except Exception:
            logger.debug("Serial buffer reset not supported", exc_info=True)

    def _exchange_command(self, command: str, expect_reply: bool = True) -> str:
        if not self._serial:
            raise RuntimeError("ESP32 not connected")

        with self._serial_lock:
            payload = f"{command.strip()}\n".encode("utf-8")
            self._serial.write(payload)
            self._serial.flush()
            if not expect_reply:
                return ""
            response = self._serial.readline()

        if not response:
            raise RuntimeError(f"No reply from ESP32 for command {command!r}")
        return response.decode("utf-8", errors="replace").strip()

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
            with self._file_lock, open(self.data_file, "w", newline="") as fh:
                writer = csv.DictWriter(fh, fieldnames=self.FIELDNAMES)
                writer.writeheader()
            logger.info("Created CSV file: %s", self.data_file)

    def _write_header_if_missing(self) -> None:
        if not self.data_file.exists():
            self.init_csv()
            return
        try:
            content = self.data_file.read_text(encoding="utf-8")
            first_line = content.splitlines()[0] if content else ""
            if not first_line or all(h not in first_line for h in self.FIELDNAMES):
                with self._file_lock, open(self.data_file, "w", newline="") as fh:
                    writer = csv.DictWriter(fh, fieldnames=self.FIELDNAMES)
                    writer.writeheader()
                    if content:
                        fh.write(content)
        except Exception:
            self.init_csv()

    # ----- Reading / conversion -----
    @staticmethod
    def _analog_to_current(analog_value: int, adc_max: int = 4095, current_scale: float = 500.0) -> float:
        """Convert an ADC value to current using the device-provided scale."""
        try:
            current = (float(analog_value) * float(current_scale)) / float(adc_max)
            return round(current, 2)
        except Exception:
            return 0.0

    def _normalize_payload(self, payload: Dict[str, object]) -> Dict[str, float | str]:
        adc_max = int(payload.get("adc_max", 4095) or 4095)
        current_scale = float(payload.get("current_scale", 500.0) or 500.0)
        values: Dict[str, float | str] = {}

        for field in self.FIELDNAMES:
            if field == "time":
                continue

            if field in payload:
                try:
                    values[field] = round(float(payload[field]), 2)
                except Exception:
                    values[field] = 0.0
                continue

            raw_key = f"raw_{field}"
            if raw_key in payload:
                values[field] = self._analog_to_current(payload[raw_key], adc_max=adc_max, current_scale=current_scale)
            else:
                values[field] = 0.0

        values["time"] = str(payload.get("time") or time.strftime("%H:%M:%S"))
        return values

    def _request_measurements(self) -> Dict[str, float | str]:
        if not _HAS_SERIAL or not self.connected or self._serial is None:
            raise RuntimeError("ESP32 not connected")

        raw_reply = self._exchange_command("READ", expect_reply=True)
        if not raw_reply:
            raise RuntimeError("Empty response from ESP32")

        try:
            payload = json.loads(raw_reply)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Invalid JSON from ESP32: {raw_reply!r}") from exc

        if not isinstance(payload, dict):
            raise RuntimeError(f"Unexpected payload type from ESP32: {type(payload)!r}")

        status = str(payload.get("status", "ok")).lower()
        if status not in {"ok", "ready"}:
            raise RuntimeError(f"ESP32 returned error status: {status}")

        return self._normalize_payload(payload)

    def read_values(self) -> Dict[str, float | str]:
        """Read one measurement snapshot from the ESP32.

        Raises RuntimeError if read fails.
        """
        try:
            vals = self._request_measurements()
            self._last_values = vals
            return vals
        except Exception as exc:
            self.connected = False
            raise RuntimeError(str(exc)) from exc

    # ----- CSV write -----
    def write_to_csv(self, data: Optional[Dict[str, float | str]] = None) -> None:
        data = data or self._last_values
        self._write_header_if_missing()
        with self._file_lock, open(self.data_file, "a", newline="") as fh:
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
        logger.info("Started ESP32 recording thread")

    def _record_loop(self) -> None:
        while self._running.is_set():
            try:
                if not self.connected:
                    self.reconnect(attempts=2, delay=1.0)

                try:
                    values = self.read_values()
                except RuntimeError:
                    values = {k: 0 for k in self.FIELDNAMES}
                    values["time"] = time.strftime("%H:%M:%S")

                self.write_to_csv(values)
                time.sleep(self.interval)
            except Exception as e:
                logger.exception("Unhandled error in ESP32 record loop: %s", e)
                time.sleep(1.0)

    def stop_record(self, join_timeout: float = 1.0) -> None:
        """Stop the background reading thread and disconnect the ESP32."""
        self._running.clear()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=join_timeout)
        try:
            self._disconnect()
        except Exception as e:
            logger.exception("Error during stop_record disconnect: %s", e)
        logger.info("Stopped ESP32 recording")

    # ----- Utilities -----
    def get_latest_values(self) -> Dict[str, float | str]:
        """Return the last read measurement (may be zeros if no read yet)."""
        return dict(self._last_values)


__all__ = ["ArduinoController"]
