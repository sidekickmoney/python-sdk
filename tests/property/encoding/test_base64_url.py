import hypothesis
from hypothesis import strategies

from python_sdk import encoding


@hypothesis.given(string=strategies.text(min_size=1))
def test_base64url_encode_result_does_not_contain_non_urlsafe_chars(string: str) -> None:
    data: bytes = encoding.b64url_encode(string.encode("utf-8"))
    result = data.decode("utf-8")
    assert "+" not in result
    assert "/" not in result
    assert "=" not in result


@hypothesis.given(string=strategies.text(min_size=1), padding=strategies.integers(min_value=0, max_value=100))
def test_base64url_decode_deals_with_incorrect_padding(string: str, padding: int) -> None:
    data: bytes = encoding.b64url_encode(string.encode("utf-8"))
    data += b"=" * padding
    data = encoding.b64url_decode(data)
    result: str = data.decode("utf-8")
    assert result == string
