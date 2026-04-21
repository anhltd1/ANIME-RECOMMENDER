"""
Central logging configuration for the template.

This module runs import-time setup: it ensures a ``logs/`` directory exists, creates a
timestamped log file, and wires Python's ``logging`` package so all ``get_logger()`` callers
share the same file handler and format. Import it once at process startup (or from a thin
``main`` module) before other modules emit log records.
"""

import logging
import os
from datetime import datetime

# Directory where rotated-by-timestamp log files are stored (created if missing).
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

# One file per process start: name encodes date and time so runs do not overwrite each other.
LOG_FILE = os.path.join(LOGS_DIR, f"logs_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

# Route root log records to the file; timestamp, level, and message on each line.
logging.basicConfig(
    filename=LOG_FILE,
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def get_logger(name: str) -> logging.Logger:
    """
    Return a named logger for the calling module (typically pass ``__name__``).

    The logger inherits the process-wide configuration from ``basicConfig``; per-logger
    level is set to INFO so library noise below that level stays quiet unless you change it.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
