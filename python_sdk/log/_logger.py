"""
Structured logging api's.
"""

import logging
from logging import handlers
import multiprocessing
import sys
import typing

from python_sdk import _log
from python_sdk import config


# TODO(lijok): Validate LOG_DESTINATION_ROTATING_FILE_PATH is writable
@config.config(prefix="PYTHON_SDK_LOG_")
class _Config:
    LEVEL: typing.Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    OUTPUT_STYLE: typing.Literal["MACHINE_READABLE", "HUMAN_READABLE"] = "MACHINE_READABLE"
    DESTINATION: typing.Literal["STDOUT", "STDERR", "ROTATING_FILE"] = "STDOUT"
    DESTINATION_ROTATING_FILE_PATH: typing.Optional[str] = None
    DESTINATION_ROTATING_FILE_MAX_SIZE_BYTES: int = 1073741824
    DESTINATION_ROTATING_FILE_MAX_NUMBER_OF_FILES: int = 10


# now that we have a config, set up a logger as dictated by the config
_log.set_level(level=_Config.LEVEL)

if _Config.OUTPUT_STYLE == "HUMAN_READABLE":
    _formatter = _log.StructuredLogHumanReadableFormatter()
elif _Config.OUTPUT_STYLE == "MACHINE_READABLE":
    _formatter = _log.StructuredLogMachineReadableFormatter()
else:
    # this should never happen
    _log.critical(f"Log output style {_Config.OUTPUT_STYLE} not implemented")
    sys.exit(1)

if _Config.DESTINATION == "STDOUT":
    _handler = _log.StreamHandler(stream=sys.stdout)
    _handler.setFormatter(fmt=_formatter)
elif _Config.DESTINATION == "STDERR":
    _handler = logging.StreamHandler(stream=sys.stderr)
    _handler.setFormatter(fmt=_formatter)
elif _Config.DESTINATION == "ROTATING_FILE":
    _rotating_file_handler = handlers.RotatingFileHandler(
        filename=_Config.DESTINATION_ROTATING_FILE_PATH,
        maxBytes=_Config.DESTINATION_ROTATING_FILE_MAX_SIZE_BYTES,
        backupCount=_Config.DESTINATION_ROTATING_FILE_MAX_NUMBER_OF_FILES,
        encoding="utf-8",
    )
    _rotating_file_handler.setFormatter(fmt=_formatter)
    _queue = multiprocessing.Queue(-1)
    # TODO(lijok): if registering atexit below this line, the EOFerror raised by multiprocessing disappears
    _handler = handlers.QueueHandler(queue=_queue)
    _queue_listener = handlers.QueueListener(_queue, _rotating_file_handler, respect_handler_level=True)
    _log.add_listener(listener=_queue_listener)
    _queue_listener.start()
else:
    # this should never happen
    _log.critical(f"Log destination {_Config.DESTINATION} not implemented")
    sys.exit(1)

_log.set_handlers(handlers=[_handler])
_log.set_logging_configured()

_log.info(
    "Logging configured",
    LEVEL=_Config.LEVEL,
    OUTPUT_STYLE=_Config.OUTPUT_STYLE,
    DESTINATION=_Config.DESTINATION,
    DESTINATION_ROTATING_FILE_PATH=_Config.DESTINATION_ROTATING_FILE_PATH,
    DESTINATION_ROTATING_FILE_MAX_SIZE_BYTES=_Config.DESTINATION_ROTATING_FILE_MAX_SIZE_BYTES,
    DESTINATION_ROTATING_FILE_MAX_NUMBER_OF_FILES=_Config.DESTINATION_ROTATING_FILE_MAX_NUMBER_OF_FILES,
)

critical = _log.critical
error = _log.error
warning = _log.warning
info = _log.info
debug = _log.debug
exception = _log.exception
bind = _log.bind
unbind = _log.unbind
unbind_all = _log.unbind_all
