from config.manager import Config


def test_default_config_values():
    cfg = Config()
    assert cfg.screen_width == 1920
    assert cfg.screen_height == 1080


def test_save_and_load(tmp_path):
    path = tmp_path / "config.json"
    cfg = Config(screen_width=800, screen_height=600)
    cfg.save(path=str(path))

    loaded = Config.load_default(path=str(path))
    assert loaded.screen_width == 800
    assert loaded.screen_height == 600
