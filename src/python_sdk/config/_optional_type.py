import types
import typing


def is_optional_type(data_type: type) -> bool:
    return (
        typing.get_origin(data_type) in [types.UnionType, typing.Union]
        and len(typing.get_args(data_type)) == 2
        and types.NoneType in typing.get_args(data_type)
    )
