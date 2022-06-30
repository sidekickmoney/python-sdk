"""
Structured logging api's.
"""

import logging
import multiprocessing
import sys
import typing
from logging import handlers

from python_sdk import _log
from python_sdk import config


# TODO(lijok): Validate LOG_DESTINATION_ROTATING_FILE_PATH is writable
@config.config(prefix="PYTHON_SDK_")
class _Config:
    LOG_LEVEL: typing.Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    LOG_OUTPUT_STYLE: typing.Literal["MACHINE_READABLE", "HUMAN_READABLE"] = "MACHINE_READABLE"
    LOG_DESTINATION: typing.Literal["STDOUT", "STDERR", "ROTATING_FILE"] = "STDOUT"
    LOG_DESTINATION_ROTATING_FILE_PATH: typing.Optional[str] = None
    LOG_DESTINATION_ROTATING_FILE_MAX_SIZE_BYTES: int = 1073741824
    LOG_DESTINATION_ROTATING_FILE_MAX_NUMBER_OF_FILES: int = 10


# now that we have a config, set up a logger as dictated by the config
_log.set_level(level=_Config.LOG_LEVEL)

if _Config.LOG_OUTPUT_STYLE == "HUMAN_READABLE":
    _formatter = _log.StructuredLogHumanReadableFormatter()
elif _Config.LOG_OUTPUT_STYLE == "MACHINE_READABLE":
    _formatter = _log.StructuredLogMachineReadableFormatter()
else:
    # this should never happen
    _log.critical(f"Log output style {_Config.LOG_OUTPUT_STYLE} not implemented")
    sys.exit(1)

if _Config.LOG_DESTINATION == "STDOUT":
    _handler = logging.StreamHandler(stream=sys.stdout)
    _handler.setFormatter(fmt=_formatter)
elif _Config.LOG_DESTINATION == "STDERR":
    _handler = logging.StreamHandler(stream=sys.stderr)
    _handler.setFormatter(fmt=_formatter)
elif _Config.LOG_DESTINATION == "ROTATING_FILE":
    _rotating_file_handler = handlers.RotatingFileHandler(
        filename=_Config.LOG_DESTINATION_ROTATING_FILE_PATH,
        maxBytes=_Config.LOG_DESTINATION_ROTATING_FILE_MAX_SIZE_BYTES,
        backupCount=_Config.LOG_DESTINATION_ROTATING_FILE_MAX_NUMBER_OF_FILES,
        encoding="utf-8",
    )
    _rotating_file_handler.setFormatter(fmt=_formatter)
    _queue = multiprocessing.Queue(-1)
    # TODO(lijok): if registering atexit below this line, the EOFerror raised by multiprocessing disappears
    _handler = handlers.QueueHandler(queue=_queue)
    _queue_listener = handlers.QueueListener(
        _queue, _rotating_file_handler, respect_handler_level=True
    )
    _log.add_listener(listener=_queue_listener)
    _queue_listener.start()
else:
    # this should never happen
    _log.critical(f"Log destination {_Config.LOG_DESTINATION} not implemented")
    sys.exit(1)

_log.remove_existing_handlers()
_log.add_handler(handler=_handler)

_log.set_logging_configured()

_log.info(
    "Logging configured",
    LOG_LEVEL=_Config.LOG_LEVEL,
    LOG_OUTPUT_STYLE=_Config.LOG_OUTPUT_STYLE,
    LOG_DESTINATION=_Config.LOG_DESTINATION,
    LOG_DESTINATION_ROTATING_FILE_PATH=_Config.LOG_DESTINATION_ROTATING_FILE_PATH,
    LOG_DESTINATION_ROTATING_FILE_MAX_SIZE_BYTES=_Config.LOG_DESTINATION_ROTATING_FILE_MAX_SIZE_BYTES,
    LOG_DESTINATION_ROTATING_FILE_MAX_NUMBER_OF_FILES=_Config.LOG_DESTINATION_ROTATING_FILE_MAX_NUMBER_OF_FILES,
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
