import pathlib
import typing

import pytest

from python_sdk import config
from python_sdk.config import _string_decoder

# TODO(lijok): replace as many of these as we can with property tests


def string_decodes_to_expected_result(string: str, data_type: type[typing.Any], expected_result: typing.Any) -> bool:
    try:
        result = _string_decoder.decode_string(string=string, data_type=data_type)
        return bool(result == expected_result)
    except Exception as e:
        return e.__class__ is expected_result


@pytest.mark.parametrize(
    "string,expected_result",
    [
        ("test", "test"),
        ("test,", "test,"),
        (",", ","),
        (", ", ", "),
        (" , ", " , "),
        (" ", " "),
        ("", ""),
    ],
)
def test_decode_config_value_to_string(string: str, expected_result: config.ConfigValueType | ValueError) -> None:
    data_type = str
    assert string_decodes_to_expected_result(string=string, data_type=data_type, expected_result=expected_result)


@pytest.mark.parametrize(
    "string,expected_result",
    [
        ("5", 5),
        ("5 ", 5),
        (" 5", 5),
        ("5.5", ValueError),
        ("test", ValueError),
        ("", ValueError),
        # (None, ValueError),
    ],
)
def test_decode_config_value_to_int(string: str, expected_result: config.ConfigValueType | ValueError) -> None:
    data_type = int
    assert string_decodes_to_expected_result(string=string, data_type=data_type, expected_result=expected_result)


@pytest.mark.parametrize(
    "string,expected_result",
    [
        ("5.5", 5.5),
        ("5", 5.0),
        ("5 ", 5.0),
        (" 5", 5.0),
        ("test", ValueError),
        ("", ValueError),
        # (None, ValueError),
    ],
)
def test_decode_config_value_to_float(string: str, expected_result: config.ConfigValueType | ValueError) -> None:
    data_type = float
    assert string_decodes_to_expected_result(string=string, data_type=data_type, expected_result=expected_result)


@pytest.mark.parametrize(
    "string,expected_result",
    [
        ("true", True),
        ("True", True),
        ("TRUE", True),
        ("yes", True),
        ("y", True),
        ("1", True),
        ("on", True),
        ("false", False),
        ("False", False),
        ("FALSE", False),
        ("no", False),
        ("n", False),
        ("0", False),
        ("off", False),
        ("FALSE ", False),
        (" FALSE", False),
        ("a", ValueError),
        ("", ValueError),
        # (None, ValueError),
    ],
)
def test_decode_config_value_to_bool(string: str, expected_result: config.ConfigValueType | ValueError) -> None:
    data_type = bool
    assert string_decodes_to_expected_result(string=string, data_type=data_type, expected_result=expected_result)


@pytest.mark.parametrize(
    "string,expected_result",
    [
        ('{"test": "test"}', {"test": "test"}),
        ('{"test": "test"}   ', {"test": "test"}),
        (' {"test": "test"}', {"test": "test"}),
        ("{'test': 'test'}", ValueError),
        ('{"test": "test"', ValueError),
        ("test", ValueError),
        ("1", ValueError),
        ("[]", ValueError),
        ("", ValueError),
    ],
)
def test_decode_config_value_to_dict(string: str, expected_result: config.ConfigValueType | ValueError) -> None:
    data_type = dict[str, typing.Any]
    assert string_decodes_to_expected_result(string=string, data_type=data_type, expected_result=expected_result)


@pytest.mark.parametrize(
    "string,expected_result",
    [
        ("dGVzdA==", config.Base64EncodedString("dGVzdA==")),
        ("dGVzdA== ", config.Base64EncodedString("dGVzdA==")),
        (" dGVzdA==", config.Base64EncodedString("dGVzdA==")),
        ("±!@", ValueError),
        ("test", ValueError),
        ("", ValueError),
        # (None, ValueError),
    ],
)
def test_decode_config_value_to_base64_encoded_string(
    string: str, expected_result: config.ConfigValueType | ValueError
) -> None:
    data_type = config.Base64EncodedString
    assert string_decodes_to_expected_result(string=string, data_type=data_type, expected_result=expected_result)


@pytest.mark.parametrize(
    "string,expected_result",
    [
        ("/temp", pathlib.Path("/temp")),
        ("/temp/one/two", pathlib.Path("/temp/one/two")),
    ],
)
def test_decode_config_value_to_path(string: str, expected_result: config.ConfigValueType | ValueError) -> None:
    data_type = pathlib.Path
    assert string_decodes_to_expected_result(string=string, data_type=data_type, expected_result=expected_result)


@pytest.mark.parametrize(
    "string,data_type,expected_result",
    [
        ("INFO", typing.Literal["INFO"], "INFO"),
        ("DEBUG", typing.Literal["INFO", "DEBUG"], "DEBUG"),
        ("info", typing.Literal["INFO"], ValueError),
        ("", typing.Literal["INFO"], ValueError),
        # (None, typing.Literal["INFO"], ValueError),
    ],
)
def test_decode_config_value_to_literal(
    string: str, data_type: config.ConfigValueType, expected_result: config.ConfigValueType | ValueError
) -> None:
    assert string_decodes_to_expected_result(string=string, data_type=data_type, expected_result=expected_result)


@pytest.mark.parametrize(
    "string,expected_result",
    [
        ("one,two,three", ["one", "two", "three"]),
        ("one", ["one"]),
        ('["one"]', ['["one"]']),
        ("[]", ["[]"]),
        ("one,two,three,", ["one", "two", "three"]),
        ("one,", ["one"]),
        (",one", ["one"]),
        (" one", ["one"]),
        ("one, ", ["one"]),
        ("", ValueError),
        (",", ValueError),
        (" ,", ValueError),
        (", ", ValueError),
        (" , ", ValueError),
    ],
)
def test_decode_config_value_to_list_of_str(string: str, expected_result: config.ConfigValueType | ValueError) -> None:
    data_type = list[str]
    assert string_decodes_to_expected_result(string=string, data_type=data_type, expected_result=expected_result)


@pytest.mark.parametrize(
    "string,expected_result",
    [
        ("1,2,3", [1, 2, 3]),
        ("1", [1]),
        ("1,2,3,", [1, 2, 3]),
        ("1,", [1]),
        (",1", [1]),
        (" 1", [1]),
        ("1, ", [1]),
        ("1.2,1.5", ValueError),
        ('["1"]', ValueError),
        ("[]", ValueError),
        ("[1]", ValueError),
        ("", ValueError),
        (",", ValueError),
        (" ,", ValueError),
        (", ", ValueError),
        (" , ", ValueError),
    ],
)
def test_decode_config_value_to_list_of_int(string: str, expected_result: config.ConfigValueType | ValueError) -> None:
    data_type = list[int]
    assert string_decodes_to_expected_result(string=string, data_type=data_type, expected_result=expected_result)


@pytest.mark.parametrize(
    "string,expected_result",
    [
        ("1.5,2.5,3.5", [1.5, 2.5, 3.5]),
        ("1.5", [1.5]),
        ("1.5,2.5,3.5,", [1.5, 2.5, 3.5]),
        ("1,2,3,", [1.0, 2.0, 3.0]),
        ("1.5,", [1.5]),
        (",1.5", [1.5]),
        (" 1.5", [1.5]),
        ("1.5, ", [1.5]),
        ('["1.5"]', ValueError),
        ("[]", ValueError),
        ("[1.5]", ValueError),
        ("", ValueError),
        (",", ValueError),
        (" ,", ValueError),
        (", ", ValueError),
        (" , ", ValueError),
    ],
)
def test_decode_config_value_to_list_of_float(
    string: str, expected_result: config.ConfigValueType | ValueError
) -> None:
    data_type = list[float]
    assert string_decodes_to_expected_result(string=string, data_type=data_type, expected_result=expected_result)


@pytest.mark.parametrize(
    "string,expected_result",
    [
        ("dGVzdA==,dGVzdA==,dGVzdA==", ["dGVzdA==", "dGVzdA==", "dGVzdA=="]),
        ("dGVzdA==", ["dGVzdA=="]),
        ("dGVzdA==,dGVzdA==,dGVzdA==,", ["dGVzdA==", "dGVzdA==", "dGVzdA=="]),
        ("dGVzdA==,", ["dGVzdA=="]),
        (" dGVzdA==", ["dGVzdA=="]),
        (",dGVzdA==", ["dGVzdA=="]),
        ("dGVzdA==,  ", ["dGVzdA=="]),
        ('["dGVzdA=="]', ValueError),
        ("[]", ValueError),
        ("", ValueError),
        (",", ValueError),
        (" ,", ValueError),
        (", ", ValueError),
        (" , ", ValueError),
    ],
)
def test_decode_config_value_to_list_of_base64_encoded_string(
    string: str, expected_result: config.ConfigValueType | ValueError
) -> None:
    data_type = list[config.Base64EncodedString]
    assert string_decodes_to_expected_result(string=string, data_type=data_type, expected_result=expected_result)


@pytest.mark.parametrize(
    "string,expected_result",
    [
        ("/temp,/sys", [pathlib.Path("/temp"), pathlib.Path("/sys")]),
    ],
)
def test_decode_config_value_to_list_of_paths(
    string: str, expected_result: config.ConfigValueType | ValueError
) -> None:
    data_type = list[pathlib.Path]
    assert string_decodes_to_expected_result(string=string, data_type=data_type, expected_result=expected_result)


@pytest.mark.parametrize(
    "string,data_type,expected_result",
    [
        ("INFO", list[typing.Literal["INFO"]], ["INFO"]),
        ("DEBUG", list[typing.Literal["INFO", "DEBUG"]], ["DEBUG"]),
        ("INFO,DEBUG", list[typing.Literal["INFO", "DEBUG"]], ["INFO", "DEBUG"]),
        ("info", list[typing.Literal["INFO"]], ValueError),
        ("INFO,", list[typing.Literal["INFO"]], ["INFO"]),
        ("INFO ", list[typing.Literal["INFO"]], ["INFO"]),
        (",INFO ", list[typing.Literal["INFO"]], ["INFO"]),
        (" INFO ", list[typing.Literal["INFO"]], ["INFO"]),
        ("", list[typing.Literal["INFO"]], ValueError),
        # (None, list[typing.Literal["INFO"]], ValueError),
    ],
)
def test_decode_config_value_to_list_of_literals(
    string: str, data_type: config.ConfigValueType, expected_result: config.ConfigValueType | ValueError
) -> None:
    assert string_decodes_to_expected_result(string=string, data_type=data_type, expected_result=expected_result)
