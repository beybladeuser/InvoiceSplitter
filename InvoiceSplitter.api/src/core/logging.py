import json
import logging
import os
import sys
from datetime import UTC, datetime
from typing import Any

_STANDARD_RECORD_ATTRIBUTES = frozenset(
    logging.makeLogRecord({}).__dict__.keys()
) | {"message", "asctime"}


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_entry: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=UTC
            ).isoformat(timespec="milliseconds"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "process": record.process,
            "thread": record.thread,
        }

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        if record.stack_info:
            log_entry["stack_info"] = self.formatStack(record.stack_info)

        log_entry.update(
            {
                str(key): value
                for key, value in record.__dict__.items()
                if key not in _STANDARD_RECORD_ATTRIBUTES
                and key not in log_entry
                and not (isinstance(key, str) and key.startswith("_"))
            }
        )

        return json.dumps(log_entry, ensure_ascii=False, default=str)


def _resolve_log_level(level: str | int | None) -> int:
    configured_level = os.getenv("LOG_LEVEL", "INFO") if level is None else level

    if isinstance(configured_level, int) and not isinstance(configured_level, bool):
        return configured_level

    if isinstance(configured_level, str):
        normalized_level = logging.getLevelNamesMapping().get(
            configured_level.upper()
        )
        if normalized_level is not None:
            return normalized_level

    raise ValueError(f"Invalid logging level: {configured_level!r}")


def configure_logging(level: str | int | None = None) -> None:
    resolved_level = _resolve_log_level(level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    handler.setLevel(resolved_level)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(resolved_level)

    for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()
        logger.propagate = True
        logger.setLevel(logging.NOTSET)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


__all__ = ["JsonFormatter", "configure_logging", "get_logger"]