import contextvars
import copy
import typing

_DEFAULT_CONTEXT_VALUE_FACTORY = dict
_CONTEXT: contextvars.ContextVar = contextvars.ContextVar(
    "_PYTHON_SDK_LOGGING_CONTEXT", default=_DEFAULT_CONTEXT_VALUE_FACTORY()
)


def get_context() -> dict[str, typing.Any]:
    return copy.copy(_CONTEXT.get())


def set_context(value: dict[str, typing.Any]) -> None:
    _CONTEXT.set(value)


class bind:
    local_context: dict[str, typing.Any]

    def __init__(self, **kwargs: dict[str, typing.Any]) -> None:
        self.local_context = kwargs
        set_context(get_context() | kwargs)

    def __enter__(self) -> None:
        return

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        unbind(*self.local_context.keys())


def unbind(*args: tuple[str]) -> None:
    set_context({key: val for key, val in _CONTEXT.get().items() if key not in args})


def unbind_all() -> None:
    set_context(_DEFAULT_CONTEXT_VALUE_FACTORY())
