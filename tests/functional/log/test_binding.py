import asyncio
import json
import threading
import typing

import pytest

from python_sdk import log
from python_sdk.log import _context


def test_bound_context_present_in_logs(capsys: pytest.CaptureFixture) -> None:
    log.Log.configure_logging()
    log.unbind_all()
    log.bind(user_id="123")
    log.info("test")
    captured_log = json.loads(capsys.readouterr().out)
    assert captured_log["user_id"] == "123"


def test_bound_context_present_in_logs_when_bind_used_as_context_manager(capsys: pytest.CaptureFixture) -> None:
    log.Log.configure_logging()
    log.unbind_all()
    with log.bind(user_id="123"):
        log.info("test")
    captured_log = json.loads(capsys.readouterr().out)
    assert captured_log["user_id"] == "123"


def test_bind_can_bind_multiple_values_at_once(capsys: pytest.CaptureFixture) -> None:
    log.Log.configure_logging()
    log.unbind_all()
    with log.bind(user_id="123", user_name="test"):
        log.info("test")
    captured_log = json.loads(capsys.readouterr().out)
    assert "user_id" in captured_log
    assert "user_name" in captured_log


def test_bind_automatically_unbinds_when_used_as_a_context_manager(capsys: pytest.CaptureFixture) -> None:
    log.Log.configure_logging()
    log.unbind_all()
    with log.bind(user_id="123"):
        pass
    log.info("test")
    captured_log = json.loads(capsys.readouterr().out)
    assert "user_id" not in captured_log


def test_bind_when_used_as_a_context_manager_does_not_unbdind_values_that_it_did_not_bind(
    capsys: pytest.CaptureFixture,
) -> None:
    log.Log.configure_logging()
    log.unbind_all()
    log.bind(user_name="test")
    with log.bind(user_id="123"):
        pass
    log.info("test")
    captured_log = json.loads(capsys.readouterr().out)
    assert "user_name" in captured_log


def test_unbind_unbinds_bound_value(capsys: pytest.CaptureFixture) -> None:
    log.Log.configure_logging()
    log.unbind_all()
    log.bind(user_id="123")
    log.unbind("user_id")
    log.info("test")
    captured_log = json.loads(capsys.readouterr().out)
    assert "user_id" not in captured_log


def test_unbind_unbinds_multiple_bound_value(capsys: pytest.CaptureFixture) -> None:
    log.Log.configure_logging()
    log.unbind_all()
    log.bind(user_id="123", user_name="test")
    log.unbind("user_id", "user_name")
    log.info("test")
    captured_log = json.loads(capsys.readouterr().out)
    assert "user_id" not in captured_log
    assert "user_name" not in captured_log


def test_unbind_does_not_unbding_more_values_than_asked(capsys: pytest.CaptureFixture) -> None:
    log.Log.configure_logging()
    log.unbind_all()
    log.bind(user_id="123", user_name="test")
    log.unbind("user_id")
    log.info("test")
    captured_log = json.loads(capsys.readouterr().out)
    assert "user_name" in captured_log


def test_unbind_all_unbinds_all_bound_values(capsys: pytest.CaptureFixture) -> None:
    log.Log.configure_logging()
    log.unbind_all()
    log.bind(user_id="123", user_name="123")
    log.unbind_all()
    log.info("test")
    captured_log = json.loads(capsys.readouterr().out)
    assert "user_id" not in captured_log
    assert "user_name" not in captured_log


def test_bind_overwrites_matching_keys(capsys: pytest.CaptureFixture) -> None:
    log.Log.configure_logging()
    log.unbind_all()
    with log.bind(user_id="123"):
        log.bind(user_id="456")
        log.info("test")
    captured_log = json.loads(capsys.readouterr().out)
    assert captured_log["user_id"] == "456"


def test_log_overwrites_matching_keys(capsys: pytest.CaptureFixture) -> None:
    log.Log.configure_logging()
    log.unbind_all()
    with log.bind(user_id="123"):
        log.info("test", user_id="456")
    captured_log = json.loads(capsys.readouterr().out)
    assert captured_log["user_id"] == "456"


def test_new_bindings_inside_bind_context_are_preserved_after_context_exit(capsys: pytest.CaptureFixture) -> None:
    log.Log.configure_logging()
    log.unbind_all()
    with log.bind(user_id="123"):
        log.bind(user_name="test")
    log.info("test")
    captured_log = json.loads(capsys.readouterr().out)
    assert "user_name" in captured_log


def test_bound_values_are_thread_local(capsys: pytest.CaptureFixture) -> None:
    log.Log.configure_logging()
    log.unbind_all()
    log.bind(user_id="123")

    class ContextCopy:
        def __init__(self, results: list[dict[str, typing.Any]]) -> None:
            assert _context.get_context() == {}
            log.bind(user_name="test")
            assert _context.get_context() == {"user_name": "test"}
            results.append(_context.get_context())

    results = []
    thread = threading.Thread(target=ContextCopy, kwargs={"results": results})
    thread.start()
    thread.join()
    current_thread_context = _context.get_context()
    new_thread_local_context = results[0]
    assert "user_id" in current_thread_context
    assert "user_name" not in current_thread_context
    assert "user_id" not in new_thread_local_context
    assert "user_name" in new_thread_local_context


def test_bound_values_are_async_local(capsys: pytest.CaptureFixture) -> None:
    log.Log.configure_logging()
    log.unbind_all()
    log.bind(user_id="123")

    async def binder() -> dict[str, typing.Any]:
        log.bind(user_name="test")
        return _context.get_context()

    async_local_context = asyncio.run(binder())
    current_local_context = _context.get_context()
    assert "user_id" in current_local_context
    assert "user_name" not in current_local_context
    assert "user_id" in async_local_context
    assert "user_name" in async_local_context


def test_unbinding_keys_that_are_not_bound_is_noop(capsys: pytest.CaptureFixture) -> None:
    log.Log.configure_logging()
    log.unbind_all()
    log.unbind("test")
