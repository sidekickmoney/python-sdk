import typing

import pytest

from python_sdk.config import _optional_type


@pytest.mark.parametrize(
    "data_type,expected_result",
    [
        (str | None, True),
        (int | None, True),
        (bool | None, True),
        (typing.Union[str, None], True),
        (typing.Union[int, None], True),
        (typing.Union[None, str], True),
        (typing.Union[None, str, None], True),
        (typing.Optional, False),
        (typing.Union, False),
        (typing.Any, False),
        (typing.Union[str, int], False),
        (typing.Union[str, int, None], False),
    ],
)
def test_is_optional_type(data_type: typing.Type, expected_result: bool) -> None:
    assert _optional_type.is_optional_type(data_type=data_type) is expected_result
