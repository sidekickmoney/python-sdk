"""
Base implementation of structured logging api's.
"""

import atexit
import contextlib
import contextvars
import datetime
import io
import json
import logging
import logging.handlers
import sys
import traceback
import typing

from python_sdk import utils

LOGGING_CONFIGURED: utils.BoolFlag = utils.BoolFlag()
TERMINATING: utils.BoolFlag = utils.BoolFlag()
LOG_STASH: typing.List[logging.LogRecord] = []

HANDLERS: typing.List[logging.Handler] = []
LISTENERS: typing.List[logging.handlers.QueueListener] = []

DEFAULT_CONTEXT_VALUE_FACTORY = dict
CONTEXT: contextvars.ContextVar = contextvars.ContextVar(
    "_PYTHON_SDK_LOGGING_CONTEXT", default=DEFAULT_CONTEXT_VALUE_FACTORY()
)


class _StructuredLogPreFormatter:
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

    def format(self, record: logging.LogRecord) -> typing.Dict[str, typing.Any]:
        timestamp = datetime.datetime.fromtimestamp(record.created).replace(tzinfo=datetime.timezone.utc)
        data = {"log_level": record.levelname, "message": record.msg, "timestamp": timestamp}
        if record.args:
            data["message"] = record.msg % record.args
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

        if record.exc_info and not record.exc_text:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            record.exc_text = self.format_exception(record.exc_info)
        if record.exc_text:
            data["exception"] = record.exc_text
        if record.stack_info:
            data["stack_info"] = record.stack_info

        context = getattr(record, "context", {})
        for key in context:
            if key in data:
                warning(f"Attempted to overwrite log attribute: {key}. Log attributes cannot be overwritten.")
            else:
                data[key] = context[key]

        return data

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


class StructuredLogMachineReadableFormatter(_StructuredLogPreFormatter):
    def format(self, record: logging.LogRecord) -> str:
        data = super().format(record=record)
        return json.dumps(data, default=str)


class StructuredLogHumanReadableFormatter(_StructuredLogPreFormatter):
    def format(self, record: logging.LogRecord) -> str:
        data = super().format(record=record)
        padding = max(60 - len(data["message"]), 0)
        text = f"{data['timestamp']} [{data['log_level']}\t] {data['message']} {' ' * padding}"
        for key, val in data.items():
            if key not in ["timestamp", "log_level", "message"]:
                text += f" {key}={val}"
        return text


class StreamHandler(logging.StreamHandler):
    def emit(self, record: logging.LogRecord) -> None:
        # this module is the base logging implementation, that is intended to be configured by the public "log" package
        # however, before it is actually configured, other packages may need to log i.e. the "config" package
        # therefore, in order to emit as many logs with the correct configuration as possible, until logging is
        # configured, we will write logs to a stash, which we intend to flush after logging is configured
        # in the event that the program terminates before logging is configured, say, because we encountered an error
        # during logging configuration, we will flush the logs as well

        if LOGGING_CONFIGURED or TERMINATING:
            if root_logger.isEnabledFor(level=record.levelno):
                super().emit(record=record)
        else:
            LOG_STASH.append(record)


def _merge_context(**kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
    data = kwargs
    for key, val in CONTEXT.get().items():
        data.setdefault(key, val)
    return data


def _log(
    level: int,
    message: typing.Any,
    exception: typing.Union[BaseException, bool] = None,
    _stack_level: int = 2,
    **kwargs: typing.Any,
) -> None:
    if not root_logger.isEnabledFor(level=level):
        return

    data = _merge_context(**kwargs)
    root_logger.log(level=level, msg=message, exc_info=exception, stacklevel=_stack_level, extra={"context": data})


def critical(message: typing.Any, **kwargs: typing.Any) -> None:
    _log(level=logging.CRITICAL, message=message, _stack_level=3, **kwargs)


def error(message: typing.Any, **kwargs: typing.Any) -> None:
    _log(level=logging.ERROR, message=message, _stack_level=3, **kwargs)


def warning(message: typing.Any, **kwargs: typing.Any) -> None:
    _log(level=logging.WARNING, message=message, _stack_level=3, **kwargs)


def info(message: typing.Any, **kwargs: typing.Any) -> None:
    _log(level=logging.INFO, message=message, _stack_level=3, **kwargs)


def debug(message: typing.Any, **kwargs: typing.Any) -> None:
    _log(level=logging.DEBUG, message=message, _stack_level=3, **kwargs)


def exception(message: typing.Any, exception: typing.Optional[BaseException] = None, **kwargs: typing.Any) -> None:
    _log(level=logging.ERROR, message=message, exception=exception or sys.exc_info(), _stack_level=3, **kwargs)


def bind(**kwargs: typing.Any) -> None:
    existing_context = CONTEXT.get()
    existing_context.update(kwargs)
    CONTEXT.set(existing_context)


def unbind(*args: str) -> None:
    existing_context = CONTEXT.get()
    new_context = {key: val for key, val in existing_context.items() if key not in args}
    CONTEXT.set(new_context)


def unbind_all() -> None:
    default_context = DEFAULT_CONTEXT_VALUE_FACTORY()
    CONTEXT.set(default_context)


@atexit.register
def _cleanup() -> None:
    TERMINATING.set()
    _flush_logs()
    _flush_and_close_handlers()
    _stop_listeners()


def _flush_logs() -> None:
    debug("Flushing logs", number_of_logs=len(LOG_STASH))
    while LOG_STASH:
        record = LOG_STASH.pop(0)
        for handler in HANDLERS:
            handler.emit(record=record)


def _flush_and_close_handlers() -> None:
    for handler in root_logger.handlers:
        with contextlib.suppress(ValueError):
            # handler might be closed already
            # this is only a problem when running pytest as it redirects stdout
            handler.flush()
        handler.close()


def _stop_listeners() -> None:
    for listener in LISTENERS:
        listener.stop()


def _remove_existing_handlers() -> None:
    for _existing_handler in root_logger.handlers:
        # TODO(lijok): are we messing up pytest by closing its handlers?
        _existing_handler.flush()
        _existing_handler.close()
        root_logger.removeHandler(_existing_handler)


def set_level(level: str) -> None:
    root_logger.setLevel(level=level)


def set_handlers(handlers: typing.List[logging.Handler]) -> None:
    _remove_existing_handlers()
    for handler in handlers:
        root_logger.addHandler(hdlr=handler)

    global HANDLERS
    HANDLERS = handlers


def add_listener(listener: logging.handlers.QueueListener) -> None:
    LISTENERS.append(listener)


root_logger = logging.getLogger()

# default config
set_level(level="DEBUG")
pre_config_formatter = StructuredLogMachineReadableFormatter()
pre_config_handler = StreamHandler(stream=sys.stdout)
pre_config_handler.setFormatter(fmt=pre_config_formatter)
set_handlers(handlers=[pre_config_handler])
