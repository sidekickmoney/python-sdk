import base64
import json
import pathlib
import typing


class UnvalidatedDict(dict[typing.Any, typing.Any]):
    def __init__(self, string: str) -> None:
        super().__init__()
        data = json.loads(string.strip())
        if not isinstance(data, dict):
            raise ValueError()
        for key, val in data.items():
            self[key] = val


class Base64EncodedString(str):
    """
    Uses UTF-8 encoding.
    """

    encoding: str = "utf-8"

    def __new__(cls, string: str) -> "Base64EncodedString":
        if not string:
            raise ValueError()
        base64.b64decode(string, validate=True).decode(cls.encoding)  # check it can be decoded
        return super().__new__(cls, string)

    @property
    def decoded(self) -> str:
        return base64.b64decode(self, validate=True).decode(self.encoding)


# TODO: base64encodedpemcert
# TODO: base64encodeddercert


# TODO: This does not include literals
# TODO: Use 3.10 notation
ConfigValueType: typing.TypeAlias = typing.Union[
    str,
    int,
    float,
    bool,
    UnvalidatedDict,
    Base64EncodedString,
    pathlib.Path,
    typing.List[str],
    typing.List[int],
    typing.List[float],
    typing.List[Base64EncodedString],
    typing.List[pathlib.Path],
    typing.Optional[str],
    typing.Optional[int],
    typing.Optional[float],
    typing.Optional[bool],
    typing.Optional[UnvalidatedDict],
    typing.Optional[Base64EncodedString],
    typing.Optional[pathlib.Path],
    typing.Optional[typing.List[str]],
    typing.Optional[typing.List[int]],
    typing.Optional[typing.List[float]],
    typing.Optional[typing.List[Base64EncodedString]],
    typing.Optional[typing.List[pathlib.Path]],
]
