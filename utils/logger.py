import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Directory where all log files will live
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "assistant.log"


def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger instance for the given module name.
    Safe to call multiple times with the same name — will not
    duplicate handlers.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        # Already configured (e.g. this function was called again
        # for the same module) — return as-is to avoid duplicate logs.
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler: only INFO and above, so debug noise doesn't
    # clutter the terminal during normal use.
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # File handler: everything (DEBUG and above), with rotation so
    # the log file doesn't grow forever.
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger