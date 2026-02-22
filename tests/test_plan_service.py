from src.config.manager import Config
from src.services.plan_service import PlanService


def test_list_plan_files(tmp_path):
    cfg = Config()
    cfg.paths.plan_dir = tmp_path / "plans"
    svc = PlanService(cfg)

    # get_plan_dir should create and return the directory
    d = svc.get_plan_dir()
    assert d.exists()

    # create some files and ensure they are discovered
    (d / "a.jpg").write_text("x")
    (d / "b.pdf").write_text("y")

    files = svc.list_plan_files()
    names = sorted([p.name for p in files])
    assert names == ["a.jpg", "b.pdf"]
