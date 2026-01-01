import logging
import os

DEFAULT_FORMAT = "%(asctime)s - movie_rating - %(levelname)s - %(message)s"

def setup_logging() -> None:
    """
    Minimal logging setup for Phase 2.
    Logs go to stdout with timestamp, service name, level, and message.
    """
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)

    logging.basicConfig(
        level=level,
        format=DEFAULT_FORMAT,
    )

