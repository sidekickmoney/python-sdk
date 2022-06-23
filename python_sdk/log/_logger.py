"""
Structured logging api's.
"""

import atexit
import contextvars
import io
import json
import logging
import multiprocessing
import os
import sys
import traceback
import typing
from logging import handlers

# TODO(lijok): implement nested contextvars
_default_context_value_factory = dict
_context = contextvars.ContextVar(
    "_python_sdk_logging_context", default=_default_context_value_factory()
)


class _StructuredLogMachineReadableFormatter:
    def __init__(
        self,
        include_current_log_filename: bool = True,
        include_function_name: bool = True,
        include_line_number: bool = True,
        include_module_name: bool = True,
        include_module_path: bool = True,
        include_process_id: bool = True,
        include_process_name: bool = True,
        include_thread_id: bool = True,
        include_thread_name: bool = True,
    ):
        self.include_current_log_filename = include_current_log_filename
        self.include_function_name = include_function_name
        self.include_line_number = include_line_number
        self.include_module_name = include_module_name
        self.include_module_path = include_module_path
        self.include_process_id = include_process_id
        self.include_process_name = include_process_name
        self.include_thread_id = include_thread_id
        self.include_thread_name = include_thread_name

    def format(self, record: logging.LogRecord) -> str:
        data = {"log_level": record.levelname, "message": record.msg, "timestamp": record.created}
        if self.include_current_log_filename:
            data["filename"] = record.filename
        if self.include_function_name:
            data["function_name"] = record.funcName
        if self.include_line_number:
            data["line_number"] = record.lineno
        if self.include_module_name:
            data["module_name"] = record.module
        if self.include_module_path:
            data["module_path"] = record.pathname
        if self.include_process_id:
            data["process_id"] = record.process
        if self.include_process_name:
            data["process_name"] = record.processName
        if self.include_thread_id:
            data["thread_id"] = record.thread
        if self.include_thread_name:
            data["thread_name"] = record.threadName

        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.format_exception(record.exc_info)
        if record.exc_text:
            data["exception"] = record.exc_text
        if record.stack_info:
            data["stack_info"] = record.stack_info

        context = getattr(record, "context", {})
        for key in context:
            if key in data:
                # TODO(lijok): add this without causing infinite loops
                # warning(f"Attempted to overwrite log attribute: {key}. Log attributes cannot be overwritten.")
                pass
            else:
                data[key] = context[key]

        return json.dumps(data, default=str)

    # taken from logging.Formatter.formatException
    def format_exception(self, ei) -> str:
        """
        Format and return the specified exception information as a string.

        This default implementation just uses
        traceback.print_exception()
        """
        sio = io.StringIO()
        tb = ei[2]
        # See issues #9427, #1553375. Commented out for now.
        # if getattr(self, 'fullstack', False):
        #    traceback.print_stack(tb.tb_frame.f_back, file=sio)
        traceback.print_exception(ei[0], ei[1], tb, None, sio)
        s = sio.getvalue()
        sio.close()
        if s[-1:] == "\n":
            s = s[:-1]
        return s


class _StructuredLogHumanReadableFormatter(_StructuredLogMachineReadableFormatter):
    def format(self, record: logging.LogRecord) -> str:
        # TODO(lijok): make this prettier
        result = super().format(record=record)
        data = json.loads(result)
        text = f"{data['timestamp']}\t\t{data['message']}"
        for key, val in data.items():
            if key not in ["timestamp", "message"]:
                text += f" {key}={val}"
        return text


def critical(message: str, **kwargs: typing.Any) -> None:
    data = _context.get()
    data.update(kwargs)
    _root_logger.critical(msg=message, extra={"context": data})


def error(message: str, **kwargs: typing.Any) -> None:
    data = _context.get()
    data.update(kwargs)
    _root_logger.error(msg=message, extra={"context": data})


def warning(message: str, **kwargs: typing.Any) -> None:
    data = _context.get()
    data.update(kwargs)
    _root_logger.warning(msg=message, extra={"context": data})


def info(message: str, **kwargs: typing.Any) -> None:
    data = _context.get()
    data.update(kwargs)
    _root_logger.info(msg=message, extra={"context": data})


def debug(message: str, **kwargs: typing.Any) -> None:
    data = _context.get()
    data.update(kwargs)
    _root_logger.debug(msg=message, extra={"context": data})


def exception(message: str, **kwargs: typing.Any) -> None:
    # TODO: more finesse required here
    data = _context.get()
    data.update(kwargs)
    _root_logger.exception(msg=message, extra={"context": data})


def bind(**kwargs: typing.Any) -> None:
    existing_context = _context.get()
    existing_context.update(kwargs)
    _context.set(existing_context)


def unbind(*args: str) -> None:
    existing_context = _context.get()
    new_context = {key: val for key, val in existing_context.items() if key not in args}
    _context.set(new_context)


def unbind_all() -> None:
    default_context = _default_context_value_factory()
    _context.set(default_context)


@atexit.register
def _flush_handlers() -> None:
    for handler in _root_logger.handlers:
        handler.flush()
        handler.close()
    queue_listener = getattr(_root_logger, "_queue_listener", None)
    if queue_listener:
        queue_listener.stop()


_root_logger = logging.getLogger()
for _existing_handler in _root_logger.handlers:
    # some runtimes provided by some hosting platforms, such as AWS Lambda, add pre-configured
    # handlers which we want to remove
    _existing_handler.close()
    _root_logger.removeHandler(_existing_handler)

# set up a standard logger in case we fail and need to log during config below
# this logger configuration will be overwritten as soon as we're done fetching the config below
_root_logger.setLevel(level="INFO")
_pre_config_formatter = _StructuredLogMachineReadableFormatter()
_pre_config_handler = logging.StreamHandler(stream=sys.stdout)
_pre_config_handler.setFormatter(fmt=_pre_config_formatter)
_root_logger.addHandler(hdlr=_pre_config_handler)

# config
_LOG_LEVEL_OPTIONS = typing.Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
_LOG_OUTPUT_STYLE_OPTIONS = typing.Literal["MACHINE_READABLE", "HUMAN_READABLE"]
_LOG_DESTINATION_OPTIONS = typing.Literal["STDOUT", "STDERR", "ROTATING_FILE"]

_LOG_LEVEL: _LOG_LEVEL_OPTIONS = os.environ.get("PYTHON_SDK_LOG_LEVEL", "INFO").upper()
if _LOG_LEVEL not in typing.get_args(_LOG_LEVEL_OPTIONS):
    critical(
        f"LOG_LEVEL {_LOG_LEVEL} not supported. Available options: {typing.get_args(_LOG_LEVEL_OPTIONS)}"
    )
    sys.exit(1)
_LOG_OUTPUT_STYLE: _LOG_OUTPUT_STYLE_OPTIONS = os.environ.get(
    "PYTHON_SDK_LOG_OUTPUT_STYLE", "MACHINE_READABLE"
)
if _LOG_OUTPUT_STYLE not in typing.get_args(_LOG_OUTPUT_STYLE_OPTIONS):
    critical(
        f"LOG_OUTPUT_STYLE {_LOG_OUTPUT_STYLE} not supported. Available options: {typing.get_args(_LOG_OUTPUT_STYLE)}"
    )
    sys.exit(1)
_LOG_DESTINATION: _LOG_DESTINATION_OPTIONS = os.environ.get("PYTHON_SDK_LOG_DESTINATION", "STDOUT")
if _LOG_DESTINATION not in typing.get_args(_LOG_DESTINATION_OPTIONS):
    critical(
        f"LOG_DESTINATION {_LOG_DESTINATION} not supported. Available options: {typing.get_args(_LOG_DESTINATION)}"
    )
    sys.exit(1)
_LOG_DESTINATION_ROTATING_FILE_PATH: str = os.environ.get(
    "PYTHON_SDK_LOG_DESTINATION_ROTATING_FILE_PATH",
)
if _LOG_DESTINATION == "ROTATING_FILE" and not _LOG_DESTINATION_ROTATING_FILE_PATH:
    critical(
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
    critical(
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
    critical(
        f"Invalid LOG_DESTINATION_ROTATING_FILE_MAX_NUMBER_OF_FILES option "
        f"{_LOG_DESTINATION_ROTATING_FILE_MAX_NUMBER_OF_FILES}. Could not convert to int."
    )
    sys.exit(1)

# TODO(lijok): should we turn these options on?
# _LOG_DATA_INCLUDE_CURRENT_LOG_FILENAME: bool = os.environ.get(
#     "PYTHON_SDK_LOG_DATA_INCLUDE_CURRENT_LOG_FILENAME", "TRUE"
# )
# _LOG_DATA_INCLUDE_FUNCTION_NAME: bool = os.environ.get("PYTHON_SDK_LOG_DATA_INCLUDE_FUNCTION_NAME", "TRUE")
# _LOG_DATA_INCLUDE_LINE_NUMBER: bool = os.environ.get("PYTHON_SDK_LOG_DATA_INCLUDE_LINE_NUMBER", "TRUE")
# _LOG_DATA_INCLUDE_MODULE_NAME: bool = os.environ.get("PYTHON_SDK_LOG_DATA_INCLUDE_MODULE_NAME", "TRUE")
# _LOG_DATA_INCLUDE_MODULE_PATH: bool = os.environ.get("PYTHON_SDK_LOG_DATA_INCLUDE_MODULE_PATH", "TRUE")
# _LOG_DATA_INCLUDE_PROCESS_ID: bool = os.environ.get("PYTHON_SDK_LOG_DATA_INCLUDE_PROCESS_ID", "TRUE")
# _LOG_DATA_INCLUDE_PROCESS_NAME: bool = os.environ.get("PYTHON_SDK_LOG_DATA_INCLUDE_PROCESS_NAME", "TRUE")
# _LOG_DATA_INCLUDE_THREAD_ID: bool = os.environ.get("PYTHON_SDK_LOG_DATA_INCLUDE_THREAD_ID", "TRUE")
# _LOG_DATA_INCLUDE_THREAD_NAME: bool = os.environ.get("PYTHON_SDK_LOG_DATA_INCLUDE_THREAD_NAME", "TRUE")

# now that we have a config, set up a logger as dictated by the config
_root_logger.setLevel(level=_LOG_LEVEL)

if _LOG_OUTPUT_STYLE == "HUMAN_READABLE":
    _formatter = _StructuredLogHumanReadableFormatter()
elif _LOG_OUTPUT_STYLE == "MACHINE_READABLE":
    _formatter = _StructuredLogMachineReadableFormatter()
else:
    # this should never happen
    critical(f"Log output style {_LOG_OUTPUT_STYLE} not implemented")
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
    _root_logger._queue_listener = _queue_listener
    _queue_listener.start()
else:
    # this should never happen
    critical(f"Log destination {_LOG_DESTINATION} not implemented")
    sys.exit(1)

for _existing_handler in _root_logger.handlers:
    # close previously configured handlers before we mount the new ones
    _existing_handler.flush()
    _existing_handler.close()
    _root_logger.removeHandler(_existing_handler)

_root_logger.addHandler(hdlr=_handler)

info(
    "logging configured",
    LOG_LEVEL=_LOG_LEVEL,
    LOG_OUTPUT_STYLE=_LOG_OUTPUT_STYLE,
    LOG_DESTINATION=_LOG_DESTINATION,
    LOG_DESTINATION_ROTATING_FILE_PATH=_LOG_DESTINATION_ROTATING_FILE_PATH,
    LOG_DESTINATION_ROTATING_FILE_MAX_SIZE_BYTES=_LOG_DESTINATION_ROTATING_FILE_MAX_SIZE_BYTES,
    LOG_DESTINATION_ROTATING_FILE_MAX_NUMBER_OF_FILES=_LOG_DESTINATION_ROTATING_FILE_MAX_NUMBER_OF_FILES,
)
