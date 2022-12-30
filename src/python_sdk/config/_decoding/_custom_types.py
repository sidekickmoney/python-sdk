import typing

Base64EncodedString = typing.TypeVar("Base64EncodedString", bound=str)
UnvalidatedDict = typing.TypeVar("UnvalidatedDict", bound=typing.Dict[typing.Any, typing.Any])


def is_optional_type(data_type: type) -> bool:
    # typing.Optional is slightly strange in that its origin, as returned by typing.get_origin is typing.Union
    # However, typing.Optional[str] (for example) is equivalent to typing.Union[str, NoneType]
    # Therefore, to correctly distinguish between typing.Union and typing.Optional, we must check that
    # the type only has 2 arguments, and that the last argument is NoneType
    arguments = typing.get_args(data_type)
    return typing.get_origin(data_type) is typing.Union and len(arguments) == 2 and arguments[-1] is type(None)
