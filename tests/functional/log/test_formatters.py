import json

import pytest

from python_sdk import log


def test_context_embedded_in_log_message_is_yanked(capsys: pytest.CaptureFixture[str]) -> None:
    log.LogConfig.configure_logging()
    user_id = 123
    log.info(f"test {user_id=}")
    captured_log = json.loads(capsys.readouterr().out)
    assert captured_log["message"] == "test"
    assert captured_log["user_id"] == str(user_id)


def test_multiple_context_values_embedded_in_log_message_are_yanked(capsys: pytest.CaptureFixture[str]) -> None:
    log.LogConfig.configure_logging()
    user_id = 123
    user_name = "test"
    log.info(f"test {user_id=} {user_name=}")
    captured_log = json.loads(capsys.readouterr().out)
    assert captured_log["message"] == "test"
    assert captured_log["user_id"] == str(user_id)
    assert captured_log["user_name"] == user_name
