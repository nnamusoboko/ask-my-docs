import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def load_text(path: str) -> str:
    file_path = Path(path)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logger.exception("Failed to read file at %s", file_path)
        raise
    except Exception:
        logger.exception("Some error occurred while trying to read from file: %s", file_path)
        raise
