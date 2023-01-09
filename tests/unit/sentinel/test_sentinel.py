import copy
import pickle
import unittest.mock

import pytest

from python_sdk.sentinel import _sentinel


class SentinelSubclass(_sentinel.Sentinel):
    ...


Unset = _sentinel.Sentinel("Unset")
UnsetDuplicate = _sentinel.Sentinel("Unset")
UnsetInAnotherModule = _sentinel.Sentinel("Unset", module_name="some.module")
SubclassedUnset = SentinelSubclass("Unset")
Missing = _sentinel.Sentinel("Missing")


def test_sentinel_str_is_correct() -> None:
    assert str(Unset) == "<Unset>"


def test_sentinel_repr_is_correct() -> None:
    assert repr(Unset) == "<Unset>"


def test_sentinel_is_truthy() -> None:
    assert bool(Unset)


def test_sentinel_returns_singleton() -> None:
    assert UnsetDuplicate is Unset


def test_sentinel_returns_new_object_for_unique_name() -> None:
    assert Missing is not Unset


def test_sentinel_returns_new_object_for_same_name_when_module_is_different() -> None:
    assert Unset is not UnsetInAnotherModule


def test_sentinel_subclasses_are_separate() -> None:
    assert Unset.__class__ is _sentinel.Sentinel
    assert SubclassedUnset is not Unset
    assert SubclassedUnset.__class__ is SentinelSubclass


def test_sentinel_is_pickleable() -> None:
    assert pickle.loads(pickle.dumps(Unset)) is Unset


def test_sentinel_subclass_is_pickleable() -> None:
    assert pickle.loads(pickle.dumps(SubclassedUnset)) is SubclassedUnset


def test_sentinel_remains_singleton_when_copied() -> None:
    assert copy.copy(Unset) is Unset
    assert copy.deepcopy({"a": Unset})["a"] is Unset


def test_sentinel_custom_repr() -> None:
    assert repr(_sentinel.Sentinel("Test", repr="test_repr")) == "test_repr"


@unittest.mock.patch("inspect.currentframe")
def test_sentinel_throws_error_if_call_stack_not_available(currentframe_mock) -> None:
    currentframe_mock.return_value = None

    with pytest.raises(RuntimeError):
        _sentinel.Sentinel("Test")
