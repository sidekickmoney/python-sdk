import logging
import sys
import typing

from python_sdk.log import _context


def _log(
    level: int,
    message: typing.Any,
    exception: BaseException | bool | None = None,
    _stack_level: int = 2,
    **kwargs: dict[str, typing.Any],
) -> None:
    root_logger = logging.getLogger()

    # root_logger.log does this check itself.
    # However, just below this, we're doing a potentially expensive dictionary merge.
    # So, as a simple performance optimization, we run this check before we do the dictionary merge.
    if not root_logger.isEnabledFor(level=level):
        return

    data = _context.get_context() | kwargs
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
