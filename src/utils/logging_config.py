import logging
import logging.config
from pathlib import Path


def setup_logging(name: str = "glam") -> logging.Logger:
    """Idempotent logging setup; safe to call multiple times."""
    # ensure logs dir
    Path("logs").mkdir(parents=True, exist_ok=True)

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}
        },
        "handlers": {
            "console": {"class": "logging.StreamHandler", "formatter": "default"},
            "file": {
                "class": "logging.FileHandler",
                "formatter": "default",
                "filename": "logs/glam.log",
                "mode": "a"
            }
        },
        "root": {"handlers": ["console", "file"], "level": "INFO"}
    }

    logging.config.dictConfig(config)
    return logging.getLogger(name)
