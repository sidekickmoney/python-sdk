"""
Structured logging api's.
"""

import logging
import multiprocessing
import os
import sys
import typing
from logging import handlers

from python_sdk import _log

# config
_LOG_LEVEL_OPTIONS = typing.Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
_LOG_OUTPUT_STYLE_OPTIONS = typing.Literal["MACHINE_READABLE", "HUMAN_READABLE"]
_LOG_DESTINATION_OPTIONS = typing.Literal["STDOUT", "STDERR", "ROTATING_FILE"]

_LOG_LEVEL: _LOG_LEVEL_OPTIONS = os.environ.get("PYTHON_SDK_LOG_LEVEL", "INFO").upper()
if _LOG_LEVEL not in typing.get_args(_LOG_LEVEL_OPTIONS):
    _log.critical(
        f"LOG_LEVEL {_LOG_LEVEL} not supported. Available options: {typing.get_args(_LOG_LEVEL_OPTIONS)}"
    )
    sys.exit(1)
_LOG_OUTPUT_STYLE: _LOG_OUTPUT_STYLE_OPTIONS = os.environ.get(
    "PYTHON_SDK_LOG_OUTPUT_STYLE", "MACHINE_READABLE"
).upper()
if _LOG_OUTPUT_STYLE not in typing.get_args(_LOG_OUTPUT_STYLE_OPTIONS):
    _log.critical(
        f"LOG_OUTPUT_STYLE {_LOG_OUTPUT_STYLE} not supported. Available options: {typing.get_args(_LOG_OUTPUT_STYLE)}"
    )
    sys.exit(1)
_LOG_DESTINATION: _LOG_DESTINATION_OPTIONS = os.environ.get(
    "PYTHON_SDK_LOG_DESTINATION", "STDOUT"
).upper()
if _LOG_DESTINATION not in typing.get_args(_LOG_DESTINATION_OPTIONS):
    _log.critical(
        f"LOG_DESTINATION {_LOG_DESTINATION} not supported. Available options: {typing.get_args(_LOG_DESTINATION)}"
    )
    sys.exit(1)
_LOG_DESTINATION_ROTATING_FILE_PATH: str = os.environ.get(
    "PYTHON_SDK_LOG_DESTINATION_ROTATING_FILE_PATH",
)
if _LOG_DESTINATION == "ROTATING_FILE" and not _LOG_DESTINATION_ROTATING_FILE_PATH:
    _log.critical(
        f"LOG_DESTINATION_ROTATING_FILE_PATH is required when LOG_DESTINATION is set to ROTATING_FILE"
    )
    sys.exit(1)
# TODO(lijok): check that we can write to this path
_LOG_DESTINATION_ROTATING_FILE_MAX_SIZE_BYTES: int = os.environ.get(
    "PYTHON_SDK_LOG_DESTINATION_ROTATING_FILE_MAX_SIZE_BYTES", "1073741824"
)  # 1GB
try:
    _LOG_DESTINATION_ROTATING_FILE_MAX_SIZE_BYTES = int(
        _LOG_DESTINATION_ROTATING_FILE_MAX_SIZE_BYTES
    )
except ValueError:
    _log.critical(
        f"Invalid LOG_DESTINATION_ROTATING_FILE_MAX_SIZE_BYTES option {_LOG_DESTINATION_ROTATING_FILE_MAX_SIZE_BYTES}. "
        f"Could not convert to int."
    )
    sys.exit(1)
_LOG_DESTINATION_ROTATING_FILE_MAX_NUMBER_OF_FILES: int = os.environ.get(
    "PYTHON_SDK_LOG_DESTINATION_ROTATING_FILE_MAX_NUMBER_OF_FILES", "10"
)
try:
    _LOG_DESTINATION_ROTATING_FILE_MAX_NUMBER_OF_FILES = int(
        _LOG_DESTINATION_ROTATING_FILE_MAX_NUMBER_OF_FILES
    )
except ValueError:
    _log.critical(
        f"Invalid LOG_DESTINATION_ROTATING_FILE_MAX_NUMBER_OF_FILES option "
        f"{_LOG_DESTINATION_ROTATING_FILE_MAX_NUMBER_OF_FILES}. Could not convert to int."
    )
    sys.exit(1)

# now that we have a config, set up a logger as dictated by the config
_log.set_level(level=_LOG_LEVEL)

if _LOG_OUTPUT_STYLE == "HUMAN_READABLE":
    _formatter = _log.StructuredLogHumanReadableFormatter()
elif _LOG_OUTPUT_STYLE == "MACHINE_READABLE":
    _formatter = _log.StructuredLogMachineReadableFormatter()
else:
    # this should never happen
    _log.critical(f"Log output style {_LOG_OUTPUT_STYLE} not implemented")
    sys.exit(1)

if _LOG_DESTINATION == "STDOUT":
    _handler = logging.StreamHandler(stream=sys.stdout)
    _handler.setFormatter(fmt=_formatter)
elif _LOG_DESTINATION == "STDERR":
    _handler = logging.StreamHandler(stream=sys.stderr)
    _handler.setFormatter(fmt=_formatter)
elif _LOG_DESTINATION == "ROTATING_FILE":
    _rotating_file_handler = handlers.RotatingFileHandler(
        filename=_LOG_DESTINATION_ROTATING_FILE_PATH,
        maxBytes=_LOG_DESTINATION_ROTATING_FILE_MAX_SIZE_BYTES,
        backupCount=_LOG_DESTINATION_ROTATING_FILE_MAX_NUMBER_OF_FILES,
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
    _log.critical(f"Log destination {_LOG_DESTINATION} not implemented")
    sys.exit(1)

_log.remove_existing_handlers()
_log.add_handler(handler=_handler)

_log.info(
    "Logging configured",
    LOG_LEVEL=_LOG_LEVEL,
    LOG_OUTPUT_STYLE=_LOG_OUTPUT_STYLE,
    LOG_DESTINATION=_LOG_DESTINATION,
    LOG_DESTINATION_ROTATING_FILE_PATH=_LOG_DESTINATION_ROTATING_FILE_PATH,
    LOG_DESTINATION_ROTATING_FILE_MAX_SIZE_BYTES=_LOG_DESTINATION_ROTATING_FILE_MAX_SIZE_BYTES,
    LOG_DESTINATION_ROTATING_FILE_MAX_NUMBER_OF_FILES=_LOG_DESTINATION_ROTATING_FILE_MAX_NUMBER_OF_FILES,
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
