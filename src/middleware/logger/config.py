import logging

from settings import settings


def setup_logging() -> None:
    level_name = getattr(settings.app, "log_level", "DEBUG" if settings.app.debug else "INFO")
    level = getattr(logging, str(level_name).upper(), logging.INFO)

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
