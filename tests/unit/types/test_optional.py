import typing

import pytest

from python_sdk import types


@pytest.mark.parametrize(
    "data_type,expected_result",
    [
        (typing.Optional[str], True),
        (typing.Optional[int], True),
        (typing.Optional[bool], True),
        (typing.Union[str, None], True),
        (typing.Union[int, None], True),
        (typing.Optional, False),
        (typing.Union, False),
        (typing.Any, False),
        (typing.Union[str, int], False),
        (typing.Union[str, int, None], False),
        (typing.Union[None, str], False),
        (typing.Union[None, str, None], False),
    ],
)
def test_is_optional_type(data_type: typing.Type, expected_result: bool) -> None:
    assert types.is_optional_type(data_type=data_type) is expected_result
