import os
import typing

from python_sdk import config


def test_config() -> None:
    os.environ["TEST_STR"] = "test"
    os.environ["TEST_INT"] = "1"
    os.environ["TEST_FLOAT"] = "1.5"
    os.environ["TEST_BOOL"] = "TRUE"
    os.environ["TEST_UNVALIDATED_DICT"] = "{}"
    os.environ["TEST_BASE64_ENCODED_STRING"] = "dGVzdA=="
    os.environ["TEST_LIST_OF_STRS"] = "test,test"
    os.environ["TEST_LIST_OF_INTS"] = "1,1"
    os.environ["TEST_LIST_OF_FLOATS"] = "1.5,1.5"
    os.environ["TEST_LIST_OF_BASE64_ENCODED_STRINGS"] = "dGVzdA==,dGVzdA=="
    os.environ["TEST_OPTIONAL_STR"] = "test"
    os.environ["TEST_OPTIONAL_INT"] = "1"
    os.environ["TEST_OPTIONAL_FLOAT"] = "1.5"
    os.environ["TEST_OPTIONAL_BOOL"] = "TRUE"
    os.environ["TEST_OPTIONAL_UNVALIDATED_DICT"] = "{}"
    os.environ["TEST_OPTIONAL_BASE64_ENCODED_STRING"] = "dGVzdA=="
    os.environ["TEST_OPTIONAL_LIST_OF_STRS"] = "test,test"
    os.environ["TEST_OPTIONAL_LIST_OF_INTS"] = "1,1"
    os.environ["TEST_OPTIONAL_LIST_OF_FLOATS"] = "1.5,1.5"
    os.environ["TEST_OPTIONAL_LIST_OF_BASE64_ENCODED_STRINGS"] = "dGVzdA==,dGVzdA=="
    os.environ["TEST_LITERAL"] = "ONE"
    os.environ["TEST_OPTIONAL_LITERAL"] = "ONE"
    os.environ["TEST_OPTIONAL_LIST_OF_LITERALS"] = "ONE,TWO"

    @config.config(prefix="TEST_")
    class Config:
        # All of these will be set
        STR: str
        INT: int
        FLOAT: float
        BOOL: bool
        UNVALIDATED_DICT: config.UnvalidatedDict
        BASE64_ENCODED_STRING: config.Base64EncodedString
        LIST_OF_STRS: typing.List[str]
        LIST_OF_INTS: typing.List[int]
        LIST_OF_FLOATS: typing.List[float]
        LIST_OF_BASE64_ENCODED_STRINGS: typing.List[config.Base64EncodedString]
        OPTIONAL_STR: typing.Optional[str]
        OPTIONAL_INT: typing.Optional[int]
        OPTIONAL_FLOAT: typing.Optional[float]
        OPTIONAL_BOOL: typing.Optional[bool]
        OPTIONAL_UNVALIDATED_DICT: typing.Optional[config.UnvalidatedDict]
        OPTIONAL_BASE64_ENCODED_STRING: typing.Optional[config.Base64EncodedString]
        OPTIONAL_LIST_OF_STRS: typing.Optional[typing.List[str]]
        OPTIONAL_LIST_OF_INTS: typing.Optional[typing.List[int]]
        OPTIONAL_LIST_OF_FLOATS: typing.Optional[typing.List[float]]
        OPTIONAL_LIST_OF_BASE64_ENCODED_STRINGS: typing.Optional[typing.List[config.Base64EncodedString]]
        LITERAL: typing.Literal["ONE", "TWO"]
        OPTIONAL_LITERAL: typing.Optional[typing.Literal["ONE", "TWO"]]
        OPTIONAL_LIST_OF_LITERALS: typing.Optional[typing.List[typing.Literal["ONE", "TWO"]]]

        # These will not be set, but have defaults, so should pick them up
        DEFAULT_STR: str = "test"
        DEFAULT_INT: int = 1
        DEFAULT_FLOAT: float = 1.5
        DEFAULT_BOOL: bool = True
        DEFAULT_UNVALIDATED_DICT: config.UnvalidatedDict = {}
        DEFAULT_BASE64_ENCODED_STRING: config.Base64EncodedString = "dGVzdA=="
        DEFAULT_LIST_OF_STRS: typing.List[str] = ["test", "test"]
        DEFAULT_LIST_OF_INTS: typing.List[int] = [1, 1]
        DEFAULT_LIST_OF_FLOATS: typing.List[float] = [1.5, 1.5]
        DEFAULT_LIST_OF_BASE64_ENCODED_STRINGS: typing.List[config.Base64EncodedString] = [
            "dGVzdA==",
            "dGVzdA==",
        ]
        DEFAULT_OPTIONAL_STR: typing.Optional[str] = "test"
        DEFAULT_OPTIONAL_INT: typing.Optional[int] = 1
        DEFAULT_OPTIONAL_FLOAT: typing.Optional[float] = 1.5
        DEFAULT_OPTIONAL_BOOL: typing.Optional[bool] = True
        DEFAULT_OPTIONAL_UNVALIDATED_DICT: typing.Optional[config.UnvalidatedDict] = {}
        DEFAULT_OPTIONAL_BASE64_ENCODED_STRING: typing.Optional[config.Base64EncodedString] = "dGVzdA=="
        DEFAULT_OPTIONAL_LIST_OF_STRS: typing.Optional[typing.List[str]] = ["test", "test"]
        DEFAULT_OPTIONAL_LIST_OF_INTS: typing.Optional[typing.List[int]] = [1, 1]
        DEFAULT_OPTIONAL_LIST_OF_FLOATS: typing.Optional[typing.List[float]] = [1.5, 1.5]
        DEFAULT_OPTIONAL_LIST_OF_BASE64_ENCODED_STRINGS: typing.Optional[typing.List[config.Base64EncodedString]] = [
            "dGVzdA==",
            "dGVzdA==",
        ]
        DEFAULT_LITERAL: typing.Literal["ONE", "TWO"] = "ONE"
        DEFAULT_OPTIONAL_LITERAL: typing.Optional[typing.Literal["ONE", "TWO"]] = "ONE"
        DEFAULT_OPTIONAL_LIST_OF_LITERALS: typing.Optional[typing.List[typing.Literal["ONE", "TWO"]]] = ["ONE", "TWO"]

        # These will not be set, so should become Nones
        UNSET_OPTIONAL_STR: typing.Optional[str]
        UNSET_OPTIONAL_INT: typing.Optional[int]
        UNSET_OPTIONAL_FLOAT: typing.Optional[float]
        UNSET_OPTIONAL_BOOL: typing.Optional[bool]
        UNSET_OPTIONAL_UNVALIDATED_DICT: typing.Optional[config.UnvalidatedDict]
        UNSET_OPTIONAL_BASE64_ENCODED_STRING: typing.Optional[config.Base64EncodedString]
        UNSET_OPTIONAL_LIST_OF_STRS: typing.Optional[typing.List[str]]
        UNSET_OPTIONAL_LIST_OF_INTS: typing.Optional[typing.List[int]]
        UNSET_OPTIONAL_LIST_OF_FLOATS: typing.Optional[typing.List[float]]
        UNSET_OPTIONAL_LIST_OF_BASE64_ENCODED_STRINGS: typing.Optional[typing.List[config.Base64EncodedString]]
        UNSET_OPTIONAL_LITERAL: typing.Optional[typing.Literal["ONE", "TWO"]]
        UNSET_OPTIONAL_LIST_OF_LITERALS: typing.Optional[typing.List[typing.Literal["ONE", "TWO"]]]

    assert Config.STR == "test"
    assert Config.INT == 1
    assert Config.FLOAT == 1.5
    assert Config.BOOL == True
    assert Config.UNVALIDATED_DICT == {}
    assert Config.BASE64_ENCODED_STRING == "dGVzdA=="
    assert Config.LIST_OF_STRS == ["test", "test"]
    assert Config.LIST_OF_INTS == [1, 1]
    assert Config.LIST_OF_FLOATS == [1.5, 1.5]
    assert Config.LIST_OF_BASE64_ENCODED_STRINGS == ["dGVzdA==", "dGVzdA=="]
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
    assert Config.LITERAL == "ONE"
    assert Config.OPTIONAL_LITERAL == "ONE"
    assert Config.OPTIONAL_LIST_OF_LITERALS == ["ONE", "TWO"]

    assert Config.DEFAULT_STR == "test"
    assert Config.DEFAULT_INT == 1
    assert Config.DEFAULT_FLOAT == 1.5
    assert Config.DEFAULT_BOOL == True
    assert Config.DEFAULT_UNVALIDATED_DICT == {}
    assert Config.DEFAULT_BASE64_ENCODED_STRING == "dGVzdA=="
    assert Config.DEFAULT_LIST_OF_STRS == ["test", "test"]
    assert Config.DEFAULT_LIST_OF_INTS == [1, 1]
    assert Config.DEFAULT_LIST_OF_FLOATS == [1.5, 1.5]
    assert Config.DEFAULT_LIST_OF_BASE64_ENCODED_STRINGS == ["dGVzdA==", "dGVzdA=="]
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
    assert Config.DEFAULT_LITERAL == "ONE"
    assert Config.DEFAULT_OPTIONAL_LITERAL == "ONE"
    assert Config.DEFAULT_OPTIONAL_LIST_OF_LITERALS == ["ONE", "TWO"]

    assert Config.UNSET_OPTIONAL_STR == None
    assert Config.UNSET_OPTIONAL_INT == None
    assert Config.UNSET_OPTIONAL_FLOAT == None
    assert Config.UNSET_OPTIONAL_BOOL == None
    assert Config.UNSET_OPTIONAL_UNVALIDATED_DICT == None
    assert Config.UNSET_OPTIONAL_BASE64_ENCODED_STRING == None
    assert Config.UNSET_OPTIONAL_LIST_OF_STRS == None
    assert Config.UNSET_OPTIONAL_LIST_OF_INTS == None
    assert Config.UNSET_OPTIONAL_LIST_OF_FLOATS == None
    assert Config.UNSET_OPTIONAL_LIST_OF_BASE64_ENCODED_STRINGS == None
    assert Config.UNSET_OPTIONAL_LITERAL == None
    assert Config.UNSET_OPTIONAL_LIST_OF_LITERALS == None
