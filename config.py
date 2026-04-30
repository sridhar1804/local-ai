"""Centralized configuration and logging for the agent harness.

All runtime settings live here, accessed via module-level constants.
Other modules import these rather than scattering defaults across constructors.
"""

from __future__ import annotations

import logging
import sys
from json import dumps as json_dumps

from dynaconf import Dynaconf

# -- Dynaconf settings wrapper ------------------------------------------------

settings = Dynaconf(
    envvar_prefix="AGENT",
    settings_files=["settings.toml", ".secrets.toml"],
)

BASE_URL: str = settings.base_url
MODEL: str = settings.model
TIMEOUT: float = settings.timeout
LOG_DIR: str = settings.log_dir

# -- Logging ----------------------------------------------------------------

_LOG_LEVEL_MAP = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
}


class _JsonFormatter(logging.Formatter):
    """Structured JSON log formatter — one JSON object per line."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info and record.exc_info[1]:
            payload["error"] = str(record.exc_info[1])
        return json_dumps(payload, default=str)


_ROOT_HANDLER = logging.StreamHandler(sys.stderr)
_ROOT_HANDLER.setFormatter(_JsonFormatter())

_ROOT_LOGGER = logging.getLogger()
_ROOT_LOGGER.setLevel(_LOG_LEVEL_MAP.get(settings.log_level, logging.INFO))
_ROOT_LOGGER.handlers = [_ROOT_HANDLER]
