"""
Base implementation of structured logging api's.
"""

import atexit
import contextvars
import datetime
import io
import json
import logging
import logging.handlers
import sys
import traceback
import typing

_LOGGING_CONFIGURED: bool = False
_TERMINATING: bool = False
_LOG_CACHE: typing.List[typing.Tuple[int, str, typing.Union[BaseException, bool], typing.Dict[str, typing.Any]]] = []

_LISTENERS: typing.List[logging.handlers.QueueListener] = []

_DEFAULT_CONTEXT_VALUE_FACTORY = dict
_CONTEXT = contextvars.ContextVar("_PYTHON_SDK_LOGGING_CONTEXT", default=_DEFAULT_CONTEXT_VALUE_FACTORY())


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
        data = {"log_level": record.levelname, "message": record.msg, "timestamp": record.created}
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
        timestamp = datetime.datetime.fromtimestamp(data["timestamp"]).replace(microsecond=0)
        padding = max(60 - len(data["message"]), 0)
        text = f"{timestamp} [{data['log_level']}\t] {data['message']} {' ' * padding}"
        for key, val in data.items():
            if key not in ["timestamp", "log_level", "message"]:
                text += f" {key}={val}"
        return text


def _merge_context(**kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
    data = kwargs
    for key, val in _CONTEXT.get().items():
        data.setdefault(key, val)
    return data


def _log(
    level: int,
    message: typing.Any,
    exception: typing.Union[BaseException, bool] = None,
    _stack_level: int = 2,
    **kwargs: typing.Any,
) -> None:
    if not _root_logger.isEnabledFor(level=level):
        return

    data = _merge_context(**kwargs)

    # this module is the base logging implementation, that is intended to be configured by the public "log" package
    # however, before it is actually configured, other packages may need to log i.e. the "config" package
    # therefore, in order to emit as many logs with the correct configuration as possible, until logging is configured,
    # we will write logs to a cache, which we intend to flush after logging is configured
    # in the event that the program terminates before logging is configured, say, because we encountered an error
    # during logging configuration, we will flush the logs as well
    if _LOGGING_CONFIGURED or _TERMINATING:
        _root_logger.log(level=level, msg=message, exc_info=exception, stacklevel=_stack_level, extra={"context": data})
    else:
        # TODO(lijok): Here we lose stack info. We should maybe manually override?
        _LOG_CACHE.append((level, message, exception, kwargs))


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
    existing_context = _CONTEXT.get()
    existing_context.update(kwargs)
    _CONTEXT.set(existing_context)


def unbind(*args: str) -> None:
    existing_context = _CONTEXT.get()
    new_context = {key: val for key, val in existing_context.items() if key not in args}
    _CONTEXT.set(new_context)


def unbind_all() -> None:
    default_context = _DEFAULT_CONTEXT_VALUE_FACTORY()
    _CONTEXT.set(default_context)


@atexit.register
def _cleanup() -> None:
    _set_terminating_flag()
    _flush_logs()
    _flush_and_close_handlers()
    _stop_listeners()


def _flush_logs() -> None:
    while _LOG_CACHE:
        level, message, exception, kwargs = _LOG_CACHE.pop(0)
        _log(level=level, message=message, exception=exception, **kwargs)


def _flush_and_close_handlers() -> None:
    for handler in _root_logger.handlers:
        try:
            handler.flush()
        except ValueError:
            # handler might be closed already
            # this is only a problem when running pytest as it redirects stdout
            pass
        handler.close()


def _stop_listeners() -> None:
    for listener in _LISTENERS:
        listener.stop()


def set_logging_configured() -> None:
    _set_logging_configured_flag()
    _flush_logs()


def _set_logging_configured_flag() -> None:
    global _LOGGING_CONFIGURED
    _LOGGING_CONFIGURED = True


def _set_terminating_flag() -> None:
    global _TERMINATING
    _TERMINATING = True


def remove_existing_handlers() -> None:
    for _existing_handler in _root_logger.handlers:
        # TODO(lijok): are we messing up pytest by closing its handlers?
        _existing_handler.flush()
        _existing_handler.close()
        _root_logger.removeHandler(_existing_handler)


def set_level(level: str) -> None:
    _root_logger.setLevel(level=level)


def add_handler(handler: logging.Handler) -> None:
    _root_logger.addHandler(hdlr=handler)


def add_listener(listener: logging.handlers.QueueListener) -> None:
    _LISTENERS.append(listener)


_root_logger = logging.getLogger()

# some runtimes provided by some hosting platforms, such as AWS Lambda, add pre-configured
# handlers which we want to remove
remove_existing_handlers()

# default config
set_level(level="INFO")
_pre_config_formatter = StructuredLogMachineReadableFormatter()
_pre_config_handler = logging.StreamHandler(stream=sys.stdout)
_pre_config_handler.setFormatter(fmt=_pre_config_formatter)
add_handler(handler=_pre_config_handler)
