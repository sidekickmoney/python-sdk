import hypothesis
from hypothesis import strategies

from python_sdk import encoding


@hypothesis.given(s=strategies.text(min_size=1))
def test_base64url_encode_result_does_not_contain_non_urlsafe_chars(s: str) -> None:
    result = encoding.b64url_encode(s=s.encode("utf-8"))
    result = result.decode("utf-8")
    assert "+" not in result
    assert "/" not in result
    assert "=" not in result


@hypothesis.given(
    s=strategies.text(min_size=1), padding=strategies.integers(min_value=0, max_value=100)
)
def test_base64url_decode_deals_with_incorrect_padding(s: str, padding: int) -> None:
    result = encoding.b64url_encode(s=s.encode("utf-8"))
    result += b"=" * padding
    result = encoding.b64url_decode(s=result)
    result = result.decode("utf-8")
    assert result == s
