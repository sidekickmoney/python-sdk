import contextvars
import typing

_DEFAULT_CONTEXT_VALUE_FACTORY = dict
_CONTEXT: contextvars.ContextVar = contextvars.ContextVar(
    "_PYTHON_SDK_LOGGING_CONTEXT", default=_DEFAULT_CONTEXT_VALUE_FACTORY()
)


def get_context() -> dict[str, typing.Any]:
    return _CONTEXT.get()


class bind:
    local_context: dict[str, typing.Any]

    def __init__(self, **kwargs: dict[str, typing.Any]) -> None:
        self.local_context = kwargs
        existing_context = _CONTEXT.get()
        existing_context.update(kwargs)
        _CONTEXT.set(existing_context)

    def __enter__(self) -> None:
        return

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        unbind(*self.local_context.keys())


def unbind(*args: tuple[str]) -> None:
    existing_context = _CONTEXT.get()
    new_context = {key: val for key, val in existing_context.items() if key not in args}
    _CONTEXT.set(new_context)


def unbind_all() -> None:
    default_context = _DEFAULT_CONTEXT_VALUE_FACTORY()
    _CONTEXT.set(default_context)
