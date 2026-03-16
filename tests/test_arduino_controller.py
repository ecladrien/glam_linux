import json
from types import SimpleNamespace

from src.config.manager import Config
from src.hardware import arduino_controller as controller_module
from src.hardware.arduino_controller import ArduinoController


class FakeSerial:
    def __init__(self, *args, **kwargs):
        self.closed = False
        self.last_command = ""

    def close(self):
        self.closed = True

    def flush(self):
        return None

    def write(self, payload):
        self.last_command = payload.decode("utf-8").strip()
        return len(payload)

    def readline(self):
        if self.last_command == "PING":
            return b"PONG\n"
        if self.last_command == "READ":
            return json.dumps(
                {
                    "status": "ok",
                    "neutre": 1.25,
                    "phase1": 2.5,
                    "phase2": 3.75,
                    "phase3": 4.0,
                    "time": "12:34:56",
                }
            ).encode("utf-8") + b"\n"
        return b""

    def reset_input_buffer(self):
        return None

    def reset_output_buffer(self):
        return None


class FakeRawSerial(FakeSerial):
    def readline(self):
        if self.last_command == "PING":
            return b"PONG\n"
        if self.last_command == "READ":
            return json.dumps(
                {
                    "status": "ok",
                    "adc_max": 4095,
                    "current_scale": 500.0,
                    "raw_neutre": 0,
                    "raw_phase1": 1024,
                    "raw_phase2": 2048,
                    "raw_phase3": 4095,
                }
            ).encode("utf-8") + b"\n"
        return b""


def build_config(tmp_path):
    cfg = Config()
    cfg.paths.data_file = tmp_path / "measurements.csv"
    cfg.hardware.arduino_port = "/dev/ttyUSB0"
    cfg.hardware.serial_baudrate = 115200
    cfg.hardware.serial_timeout = 0.1
    cfg.hardware.esp32_boot_delay = 0.0
    return cfg


def test_read_values_from_esp32_json(monkeypatch, tmp_path):
    monkeypatch.setattr(controller_module, "_HAS_SERIAL", True)
    monkeypatch.setattr(controller_module, "serial", SimpleNamespace(Serial=FakeSerial))

    ctrl = ArduinoController(config=build_config(tmp_path))

    values = ctrl.read_values()

    assert ctrl.connected is True
    assert values == {
        "neutre": 1.25,
        "phase1": 2.5,
        "phase2": 3.75,
        "phase3": 4.0,
        "time": "12:34:56",
    }


def test_read_values_from_raw_payload(monkeypatch, tmp_path):
    monkeypatch.setattr(controller_module, "_HAS_SERIAL", True)
    monkeypatch.setattr(controller_module, "serial", SimpleNamespace(Serial=FakeRawSerial))

    ctrl = ArduinoController(config=build_config(tmp_path))

    values = ctrl.read_values()

    assert values["neutre"] == 0.0
    assert values["phase1"] == 125.03
    assert values["phase2"] == 250.06
    assert values["phase3"] == 500.0
    assert isinstance(values["time"], str)