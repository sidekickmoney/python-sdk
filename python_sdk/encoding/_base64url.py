import base64
import typing


def b64url_encode(s: bytes) -> bytes:
    return base64.urlsafe_b64encode(s=s).rstrip(b"=")


def b64url_decode(s: typing.Union[bytes, str]) -> bytes:
    padding_character = b"=" if isinstance(s, bytes) else "="
    padding = (len(s) % 4) * padding_character
    padded = s + padding
    return base64.urlsafe_b64decode(padded)
