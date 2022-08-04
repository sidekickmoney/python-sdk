"""
Module for decoding config values.
The @config decorator supports a number of types, all of which are listed in the code below.
"""
import base64
import json
import typing

from . import _optional

_ENCODED_LIST_SEPARATOR = ","

Base64EncodedString = typing.TypeVar("Base64EncodedString", bound=str)
UnvalidatedDict = typing.TypeVar("UnvalidatedDict", bound=typing.Dict[typing.Any, typing.Any])


def _str_to_str(string: str) -> str:
    if not string:
        raise ValueError()
    return str(string)


def _str_to_int(string: str) -> int:
    if string.strip() != string:
        raise ValueError("Leading or trailing whitespace detected")
    return int(string)


def _str_to_float(string: str) -> float:
    if string.strip() != string:
        raise ValueError("Leading or trailing whitespace detected")
    return float(string)


def _str_to_bool(string: str) -> bool:
    # NOTE(lijok): Given the intolerance of the other decoders to typos, casing
    # and trailing whitespace, us being case-agnostic here is inconsistent with
    # the wider philosophy.
    # However, we've chosen to allow this due to how common case-agnostic bools are
    # in declarative configurations.
    if string.strip() != string:
        raise ValueError("Leading or trailing whitespace detected")
    normalized_string = string.upper()
    if normalized_string == "TRUE":
        return True
    elif normalized_string == "FALSE":
        return False
    raise ValueError()


def _str_to_unvalidated_dict(string: str) -> typing.Dict[typing.Any, typing.Any]:
    if string.strip() != string:
        raise ValueError("Leading or trailing whitespace detected")
    data = json.loads(string)
    if not isinstance(data, dict):
        raise ValueError()
    return data


def _str_to_base64_encoded_string(string: str) -> str:
    if string.strip() != string:
        raise ValueError("Leading or trailing whitespace detected")
    if not string:
        raise ValueError()
    base64.b64decode(string, validate=True).decode("utf-8")  # check it can be decoded
    return string


def _str_to_literal(string: str, literal: typing.Type) -> str:
    if string.strip() != string:
        raise ValueError("Leading or trailing whitespace detected")
    if string not in typing.get_args(literal):
        raise ValueError()
    return string


def _str_to_list_of_strs(string: str) -> typing.List[str]:
    if string.strip().strip(_ENCODED_LIST_SEPARATOR) != string:
        raise ValueError("Leading or trailing whitespace or comma detected")
    if not string:
        raise ValueError()
    return string.split(_ENCODED_LIST_SEPARATOR)


def _str_to_list_of_ints(string: str) -> typing.List[int]:
    if string.strip().strip(_ENCODED_LIST_SEPARATOR) != string:
        raise ValueError("Leading or trailing whitespace or comma detected")
    if not string:
        raise ValueError()
    return [int(i) for i in string.split(_ENCODED_LIST_SEPARATOR)]


def _str_to_list_of_floats(string: str) -> typing.List[float]:
    if string.strip().strip(_ENCODED_LIST_SEPARATOR) != string:
        raise ValueError("Leading or trailing whitespace or comma detected")
    if not string:
        raise ValueError()
    return [float(i) for i in string.split(_ENCODED_LIST_SEPARATOR)]


def _str_to_list_of_base64_encoded_strings(string: str) -> typing.List[str]:
    if string.strip().strip(_ENCODED_LIST_SEPARATOR) != string:
        raise ValueError("Leading or trailing whitespace or comma detected")
    if not string:
        raise ValueError()
    maybe_base64_encoded_strings = string.split(_ENCODED_LIST_SEPARATOR)
    for i in maybe_base64_encoded_strings:
        # check they can be decoded
        base64.b64decode(i, validate=True).decode("utf-8")
    return maybe_base64_encoded_strings


def _str_to_list_of_literals(string: str, literal: typing.Type) -> typing.List[str]:
    if string.strip().strip(_ENCODED_LIST_SEPARATOR) != string:
        raise ValueError("Leading or trailing whitespace or comma detected")
    if not string:
        raise ValueError()
    strings = string.split(_ENCODED_LIST_SEPARATOR)
    literal_options = typing.get_args(literal)
    for string in strings:
        if string not in literal_options:
            raise ValueError()
    return strings


def _str_to_optional_str(string: typing.Optional[str]) -> typing.Optional[str]:
    if string:
        return string


def _str_to_optional_int(string: typing.Optional[str]) -> typing.Optional[int]:
    if string:
        return _str_to_int(string=string)
    return None


def _str_to_optional_float(string: typing.Optional[str]) -> typing.Optional[float]:
    if string:
        return _str_to_float(string=string)
    return None


def _str_to_optional_bool(string: typing.Optional[str]) -> typing.Optional[bool]:
    if string:
        return _str_to_bool(string=string)
    return None


def _str_to_optional_unvalidated_dict(
    string: typing.Optional[str],
) -> typing.Optional[typing.Dict[typing.Any, typing.Any]]:
    if string:
        return _str_to_unvalidated_dict(string=string)
    return None


def _str_to_optional_base64_encoded_string(string: typing.Optional[str]) -> typing.Optional[str]:
    if string:
        return _str_to_base64_encoded_string(string=string)
    return None


def _str_to_optional_literal(string: typing.Optional[str], literal: typing.Type) -> typing.Optional[str]:
    if string:
        return _str_to_literal(string=string, literal=literal)
    return None


def _str_to_optional_list_of_strs(
    string: typing.Optional[str],
) -> typing.Optional[typing.List[str]]:
    if string:
        return _str_to_list_of_strs(string=string)
    return None


def _str_to_optional_list_of_ints(
    string: typing.Optional[str],
) -> typing.Optional[typing.List[int]]:
    if string:
        return _str_to_list_of_ints(string=string)
    return None


def _str_to_optional_list_of_floats(
    string: typing.Optional[str],
) -> typing.Optional[typing.List[float]]:
    if string:
        return _str_to_list_of_floats(string=string)
    return None


def _str_to_optional_list_of_base64_encoded_strings(
    string: typing.Optional[str],
) -> typing.Optional[typing.List[str]]:
    if string:
        return _str_to_list_of_base64_encoded_strings(string=string)
    return None


def _str_to_optional_list_of_literals(
    string: typing.Optional[str], literal: typing.Type
) -> typing.Optional[typing.List[str]]:
    if string:
        return _str_to_list_of_literals(string=string, literal=literal)
    return None


# in addition to the below, we support Literal[...], List[Literal[...]] and Optional[List[Literal[...]]]
# however, as they are variadic types, we can't have them in the lookup table below
# therefore, functions in this module will have to provide special support for Literal
_DECODERS_LOOKUP_TABLE = {
    # primitives
    str: _str_to_str,
    int: _str_to_int,
    float: _str_to_float,
    bool: _str_to_bool,
    UnvalidatedDict: _str_to_unvalidated_dict,
    Base64EncodedString: _str_to_base64_encoded_string,
    # lists of primitives
    typing.List[str]: _str_to_list_of_strs,
    typing.List[int]: _str_to_list_of_ints,
    typing.List[float]: _str_to_list_of_floats,
    typing.List[Base64EncodedString]: _str_to_list_of_base64_encoded_strings,
    # optional primitives
    typing.Optional[str]: _str_to_optional_str,
    typing.Optional[int]: _str_to_optional_int,
    typing.Optional[float]: _str_to_optional_float,
    typing.Optional[bool]: _str_to_optional_bool,
    typing.Optional[UnvalidatedDict]: _str_to_optional_unvalidated_dict,
    typing.Optional[Base64EncodedString]: _str_to_optional_base64_encoded_string,
    # optional lists of primitives
    typing.Optional[typing.List[str]]: _str_to_optional_list_of_strs,
    typing.Optional[typing.List[int]]: _str_to_optional_list_of_ints,
    typing.Optional[typing.List[float]]: _str_to_optional_list_of_floats,
    typing.Optional[typing.List[Base64EncodedString]]: _str_to_optional_list_of_base64_encoded_strings,
}


def type_is_supported(data_type: typing.Type) -> bool:
    if data_type in _DECODERS_LOOKUP_TABLE:
        return True
    if (
        _is_literal(data_type=data_type)
        or _is_optional_literal(data_type=data_type)
        or _is_list_of_literals(data_type=data_type)
        or _is_optional_list_of_literals(data_type=data_type)
    ):
        return True
    return False


def _is_literal(data_type: typing.Type) -> bool:
    # for a type to be considered Literal it must be a typing.Literal with all arguments
    # being upper-cased strings
    if typing.get_origin(data_type) == typing.Literal:
        literal_options = list(typing.get_args(data_type))
        if len({type(arg) for arg in literal_options}) == 1:
            if type(literal_options[0]) == str:

                literal_options_uppercased = [literal_option.upper() for literal_option in literal_options]
                if literal_options_uppercased == literal_options:
                    return True
    return False


def _is_optional_literal(data_type: typing.Type) -> bool:
    return typing.get_origin(data_type) == typing.Union and _is_literal(data_type=typing.get_args(data_type)[0])


def _is_list_of_literals(data_type: typing.Type) -> bool:
    return typing.get_origin(data_type) == list and _is_literal(data_type=typing.get_args(data_type)[0])


def _is_optional_list_of_literals(data_type: typing.Type) -> bool:
    return typing.get_origin(data_type) == typing.Union and _is_list_of_literals(
        data_type=typing.get_args(data_type)[0]
    )


def _decode_str(string: str, data_type: typing.Type) -> typing.Any:
    if _is_literal(data_type=data_type):
        return _str_to_literal(string=string, literal=data_type)
    elif _is_optional_literal(data_type=data_type):
        return _str_to_optional_literal(string=string, literal=typing.get_args(data_type)[0])
    elif _is_list_of_literals(data_type=data_type):
        return _str_to_list_of_literals(string=string, literal=typing.get_args(data_type)[0])
    elif _is_optional_list_of_literals(data_type=data_type):
        return _str_to_optional_list_of_literals(
            string=string,
            literal=typing.get_args(typing.get_args(data_type)[0])[0],
        )
    else:
        decoder = _DECODERS_LOOKUP_TABLE[data_type]
        return decoder(string=string)


def decode_config_value(maybe_string: typing.Optional[str], data_type: typing.Type) -> typing.Any:
    if not type_is_supported(data_type=data_type):
        raise TypeError(f"Type {data_type} is not supported")
    if maybe_string is None and not _optional._is_optional_type(data_type=data_type):
        # got None for a non-optional type
        raise ValueError()
    string = typing.cast(str, maybe_string)  # TODO(lijok): fix this hack
    return _decode_str(string=string, data_type=data_type)
