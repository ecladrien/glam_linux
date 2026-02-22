from src.config.manager import Config
from src.services.measurement_service import MeasurementService
from pathlib import Path


def test_copy_and_reset(tmp_path):
    cfg = Config()
    cfg.paths.data_file = tmp_path / "measurements.csv"
    svc = MeasurementService(cfg)

    # ensure parent directory created (file may be created later)
    df = svc.get_data_file()
    assert df.parent.exists()

    # write some content and copy it
    df.write_text("a,b,c")
    dest = tmp_path / "out" / "copy.csv"
    svc.copy_to(df, dest)
    assert dest.exists()

    # reset file and ensure header present
    svc.reset_file(df)
    text = df.read_text()
    assert text.strip().startswith('neutre') or text.strip().startswith('time')
