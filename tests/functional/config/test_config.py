import os
import pathlib
import typing

from python_sdk import config


def test_config() -> None:
    configuration = {
        "TEST_STR": "test",
        "TEST_INT": "1",
        "TEST_FLOAT": "1.5",
        "TEST_BOOL": "TRUE",
        "TEST_UNVALIDATED_DICT": "{}",
        "TEST_BASE64_ENCODED_STRING": "dGVzdA==",
        "TEST_PATH": "/tmp",
        "TEST_LIST_OF_STRS": "test,test",
        "TEST_LIST_OF_INTS": "1,1",
        "TEST_LIST_OF_FLOATS": "1.5,1.5",
        "TEST_LIST_OF_BASE64_ENCODED_STRINGS": "dGVzdA==,dGVzdA==",
        "TEST_LIST_OF_PATHS": "/tmp,/opt",
        "TEST_OPTIONAL_STR": "test",
        "TEST_OPTIONAL_INT": "1",
        "TEST_OPTIONAL_FLOAT": "1.5",
        "TEST_OPTIONAL_BOOL": "TRUE",
        "TEST_OPTIONAL_UNVALIDATED_DICT": "{}",
        "TEST_OPTIONAL_BASE64_ENCODED_STRING": "dGVzdA==",
        "TEST_OPTIONAL_LIST_OF_STRS": "test,test",
        "TEST_OPTIONAL_LIST_OF_INTS": "1,1",
        "TEST_OPTIONAL_LIST_OF_FLOATS": "1.5,1.5",
        "TEST_OPTIONAL_LIST_OF_BASE64_ENCODED_STRINGS": "dGVzdA==,dGVzdA==",
        "TEST_OPTIONAL_LIST_OF_PATHS": "/tmp,/opt",
        "TEST_LITERAL": "ONE",
        "TEST_OPTIONAL_LITERAL": "ONE",
        "TEST_OPTIONAL_LIST_OF_LITERALS": "ONE,TWO",
    }
    os.environ.update(configuration)

    class Config(config.Config, option_prefix="TEST_"):
        # All of these will be set
        STR: str = config.Option()
        INT: int = config.Option()
        FLOAT: float = config.Option()
        BOOL: bool = config.Option()
        UNVALIDATED_DICT: config.UnvalidatedDict = config.Option()
        BASE64_ENCODED_STRING: config.Base64EncodedString = config.Option()
        PATH: pathlib.Path = config.Option()
        LIST_OF_STRS: typing.List[str] = config.Option()
        LIST_OF_INTS: typing.List[int] = config.Option()
        LIST_OF_FLOATS: typing.List[float] = config.Option()
        LIST_OF_BASE64_ENCODED_STRINGS: typing.List[config.Base64EncodedString] = config.Option()
        LIST_OF_PATHS: typing.List[pathlib.Path] = config.Option()
        OPTIONAL_STR: str | None = config.Option()
        OPTIONAL_INT: int | None = config.Option()
        OPTIONAL_FLOAT: float | None = config.Option()
        OPTIONAL_BOOL: bool | None = config.Option()
        OPTIONAL_UNVALIDATED_DICT: config.UnvalidatedDict | None = config.Option()
        OPTIONAL_BASE64_ENCODED_STRING: config.Base64EncodedString | None = config.Option()
        OPTIONAL_LIST_OF_STRS: typing.List[str] | None = config.Option()
        OPTIONAL_LIST_OF_INTS: typing.List[int] | None = config.Option()
        OPTIONAL_LIST_OF_FLOATS: typing.List[float] | None = config.Option()
        OPTIONAL_LIST_OF_BASE64_ENCODED_STRINGS: typing.Optional[
            typing.List[config.Base64EncodedString]
        ] = config.Option()
        OPTIONAL_LIST_OF_PATHS: typing.List[pathlib.Path] | None = config.Option()
        LITERAL: typing.Literal["ONE", "TWO"] = config.Option()
        OPTIONAL_LITERAL: typing.Literal["ONE", "TWO"] | None = config.Option()
        OPTIONAL_LIST_OF_LITERALS: typing.List[typing.Literal["ONE", "TWO"]] | None = config.Option()

        # These will not be set, but have defaults, so should pick them up
        DEFAULT_STR: str = config.Option(default="test")
        DEFAULT_INT: int = config.Option(default=1)
        DEFAULT_FLOAT: float = config.Option(default=1.5)
        DEFAULT_BOOL: bool = config.Option(default=True)
        DEFAULT_UNVALIDATED_DICT: config.UnvalidatedDict = config.Option(default={})
        DEFAULT_BASE64_ENCODED_STRING: config.Base64EncodedString = config.Option(default="dGVzdA==")
        DEFAULT_PATH: pathlib.Path = config.Option(default=pathlib.Path("/tmp"))
        DEFAULT_LIST_OF_STRS: typing.List[str] = config.Option(default=["test", "test"])
        DEFAULT_LIST_OF_INTS: typing.List[int] = config.Option(default=[1, 1])
        DEFAULT_LIST_OF_FLOATS: typing.List[float] = config.Option(default=[1.5, 1.5])
        DEFAULT_LIST_OF_BASE64_ENCODED_STRINGS: typing.List[config.Base64EncodedString] = config.Option(
            default=[
                "dGVzdA==",
                "dGVzdA==",
            ]
        )
        DEFAULT_LIST_OF_PATHS: typing.List[pathlib.Path] = config.Option(
            default=[pathlib.Path("/tmp"), pathlib.Path("/opt")]
        )
        DEFAULT_OPTIONAL_STR: str | None = config.Option(default="test")
        DEFAULT_OPTIONAL_INT: int | None = config.Option(default=1)
        DEFAULT_OPTIONAL_FLOAT: float | None = config.Option(default=1.5)
        DEFAULT_OPTIONAL_BOOL: bool | None = config.Option(default=True)
        DEFAULT_OPTIONAL_UNVALIDATED_DICT: config.UnvalidatedDict | None = config.Option(default={})
        DEFAULT_OPTIONAL_BASE64_ENCODED_STRING: config.Base64EncodedString | None = config.Option(default="dGVzdA==")
        DEFAULT_OPTIONAL_LIST_OF_STRS: typing.List[str] | None = config.Option(default=["test", "test"])
        DEFAULT_OPTIONAL_LIST_OF_INTS: typing.List[int] | None = config.Option(default=[1, 1])
        DEFAULT_OPTIONAL_LIST_OF_FLOATS: typing.List[float] | None = config.Option(default=[1.5, 1.5])
        DEFAULT_OPTIONAL_LIST_OF_BASE64_ENCODED_STRINGS: typing.Optional[
            typing.List[config.Base64EncodedString]
        ] = config.Option(
            default=[
                "dGVzdA==",
                "dGVzdA==",
            ]
        )
        DEFAULT_OPTIONAL_LIST_OF_PATHS: typing.List[pathlib.Path] | None = config.Option(
            default=[
                pathlib.Path("/tmp"),
                pathlib.Path("/opt"),
            ]
        )
        DEFAULT_LITERAL: typing.Literal["ONE", "TWO"] = config.Option(default="ONE")
        DEFAULT_OPTIONAL_LITERAL: typing.Literal["ONE", "TWO"] | None = config.Option(default="ONE")
        DEFAULT_OPTIONAL_LIST_OF_LITERALS: typing.List[typing.Literal["ONE", "TWO"]] | None = config.Option(
            default=["ONE", "TWO"]
        )

        # These will not be set, so should become Nones
        UNSET_OPTIONAL_STR: str | None = config.Option()
        UNSET_OPTIONAL_INT: int | None = config.Option()
        UNSET_OPTIONAL_FLOAT: float | None = config.Option()
        UNSET_OPTIONAL_BOOL: bool | None = config.Option()
        UNSET_OPTIONAL_UNVALIDATED_DICT: config.UnvalidatedDict | None = config.Option()
        UNSET_OPTIONAL_BASE64_ENCODED_STRING: config.Base64EncodedString | None = config.Option()
        UNSET_OPTIONAL_PATH: pathlib.Path | None = config.Option()
        UNSET_OPTIONAL_LIST_OF_STRS: typing.List[str] | None = config.Option()
        UNSET_OPTIONAL_LIST_OF_INTS: typing.List[int] | None = config.Option()
        UNSET_OPTIONAL_LIST_OF_FLOATS: typing.List[float] | None = config.Option()
        UNSET_OPTIONAL_LIST_OF_BASE64_ENCODED_STRINGS: typing.Optional[
            typing.List[config.Base64EncodedString]
        ] = config.Option()
        UNSET_OPTIONAL_LIST_OF_PATHS: typing.List[pathlib.Path] | None = config.Option()
        UNSET_OPTIONAL_LITERAL: typing.Literal["ONE", "TWO"] | None = config.Option()
        UNSET_OPTIONAL_LIST_OF_LITERALS: typing.List[typing.Literal["ONE", "TWO"]] | None = config.Option()

    assert Config.STR == "test"
    assert Config.INT == 1
    assert Config.FLOAT == 1.5
    assert Config.BOOL == True
    assert Config.UNVALIDATED_DICT == {}
    assert Config.BASE64_ENCODED_STRING == "dGVzdA=="
    assert Config.PATH == pathlib.Path("/tmp")
    assert Config.LIST_OF_STRS == ["test", "test"]
    assert Config.LIST_OF_INTS == [1, 1]
    assert Config.LIST_OF_FLOATS == [1.5, 1.5]
    assert Config.LIST_OF_BASE64_ENCODED_STRINGS == ["dGVzdA==", "dGVzdA=="]
    assert Config.LIST_OF_PATHS == [pathlib.Path("/tmp"), pathlib.Path("/opt")]
    assert Config.OPTIONAL_STR == "test"
    assert Config.OPTIONAL_INT == 1
    assert Config.OPTIONAL_FLOAT == 1.5
    assert Config.OPTIONAL_BOOL == True
    assert Config.OPTIONAL_UNVALIDATED_DICT == {}
    assert Config.OPTIONAL_BASE64_ENCODED_STRING == "dGVzdA=="
    assert Config.OPTIONAL_LIST_OF_STRS == ["test", "test"]
    assert Config.OPTIONAL_LIST_OF_INTS == [1, 1]
    assert Config.OPTIONAL_LIST_OF_FLOATS == [1.5, 1.5]
    assert Config.OPTIONAL_LIST_OF_BASE64_ENCODED_STRINGS == ["dGVzdA==", "dGVzdA=="]
    assert Config.OPTIONAL_LIST_OF_PATHS == [pathlib.Path("/tmp"), pathlib.Path("/opt")]
    assert Config.LITERAL == "ONE"
    assert Config.OPTIONAL_LITERAL == "ONE"
    assert Config.OPTIONAL_LIST_OF_LITERALS == ["ONE", "TWO"]

    assert Config.DEFAULT_STR == "test"
    assert Config.DEFAULT_INT == 1
    assert Config.DEFAULT_FLOAT == 1.5
    assert Config.DEFAULT_BOOL == True
    assert Config.DEFAULT_UNVALIDATED_DICT == {}
    assert Config.DEFAULT_BASE64_ENCODED_STRING == "dGVzdA=="
    assert Config.DEFAULT_PATH == pathlib.Path("/tmp")
    assert Config.DEFAULT_LIST_OF_STRS == ["test", "test"]
    assert Config.DEFAULT_LIST_OF_INTS == [1, 1]
    assert Config.DEFAULT_LIST_OF_FLOATS == [1.5, 1.5]
    assert Config.DEFAULT_LIST_OF_BASE64_ENCODED_STRINGS == ["dGVzdA==", "dGVzdA=="]
    assert Config.DEFAULT_LIST_OF_PATHS == [pathlib.Path("/tmp"), pathlib.Path("/opt")]
    assert Config.DEFAULT_OPTIONAL_STR == "test"
    assert Config.DEFAULT_OPTIONAL_INT == 1
    assert Config.DEFAULT_OPTIONAL_FLOAT == 1.5
    assert Config.DEFAULT_OPTIONAL_BOOL == True
    assert Config.DEFAULT_OPTIONAL_UNVALIDATED_DICT == {}
    assert Config.DEFAULT_OPTIONAL_BASE64_ENCODED_STRING == "dGVzdA=="
    assert Config.DEFAULT_OPTIONAL_LIST_OF_STRS == ["test", "test"]
    assert Config.DEFAULT_OPTIONAL_LIST_OF_INTS == [1, 1]
    assert Config.DEFAULT_OPTIONAL_LIST_OF_FLOATS == [1.5, 1.5]
    assert Config.DEFAULT_OPTIONAL_LIST_OF_BASE64_ENCODED_STRINGS == ["dGVzdA==", "dGVzdA=="]
    assert Config.DEFAULT_OPTIONAL_LIST_OF_PATHS == [pathlib.Path("/tmp"), pathlib.Path("/opt")]
    assert Config.DEFAULT_LITERAL == "ONE"
    assert Config.DEFAULT_OPTIONAL_LITERAL == "ONE"
    assert Config.DEFAULT_OPTIONAL_LIST_OF_LITERALS == ["ONE", "TWO"]

    assert Config.UNSET_OPTIONAL_STR == None
    assert Config.UNSET_OPTIONAL_INT == None
    assert Config.UNSET_OPTIONAL_FLOAT == None
    assert Config.UNSET_OPTIONAL_BOOL == None
    assert Config.UNSET_OPTIONAL_UNVALIDATED_DICT == None
    assert Config.UNSET_OPTIONAL_BASE64_ENCODED_STRING == None
    assert Config.UNSET_OPTIONAL_PATH == None
    assert Config.UNSET_OPTIONAL_LIST_OF_STRS == None
    assert Config.UNSET_OPTIONAL_LIST_OF_INTS == None
    assert Config.UNSET_OPTIONAL_LIST_OF_FLOATS == None
    assert Config.UNSET_OPTIONAL_LIST_OF_BASE64_ENCODED_STRINGS == None
    assert Config.UNSET_OPTIONAL_LIST_OF_PATHS == None
    assert Config.UNSET_OPTIONAL_LITERAL == None
    assert Config.UNSET_OPTIONAL_LIST_OF_LITERALS == None
