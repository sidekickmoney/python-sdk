import json
import traceback

import pytest

from python_sdk import log


def test_exception_log_outside_except_block_has_correct_message(capsys: pytest.CaptureFixture) -> None:
    log.LogConfig.configure_logging()
    log.exception("test", exception=Exception("exception"))
    captured_log = json.loads(capsys.readouterr().out)
    assert captured_log["message"] == "test"


def test_exception_log_inside_except_block_has_correct_message(capsys: pytest.CaptureFixture) -> None:
    log.LogConfig.configure_logging()
    try:
        raise Exception("exception")
    except:
        log.exception("test", exception=Exception("exception"))
    captured_log = json.loads(capsys.readouterr().out)
    assert captured_log["message"] == "test"


def test_manually_passed_exception_with_no_context_outside_except_block_has_correct_exception(
    capsys: pytest.CaptureFixture,
) -> None:
    log.LogConfig.configure_logging()
    log.exception("test", exception=Exception("error"))
    captured_log = json.loads(capsys.readouterr().out)
    assert captured_log["exception"] == "Exception: error"


def test_manually_passed_exception_with_no_context_inside_except_block_has_correct_exception(
    capsys: pytest.CaptureFixture,
) -> None:
    log.LogConfig.configure_logging()
    try:
        raise Exception("exception")
    except:
        log.exception("test", exception=Exception("error"))
    captured_log = json.loads(capsys.readouterr().out)
    assert captured_log["exception"] == "Exception: error"


def test_manually_passed_exception_with_context_outside_except_block_has_correct_exception(
    capsys: pytest.CaptureFixture,
) -> None:
    log.LogConfig.configure_logging()
    try:
        raise Exception("error")
    except Exception as e:
        exception = e
    log.exception("test", exception=exception)
    captured_log = json.loads(capsys.readouterr().out)
    assert captured_log["exception"].strip() == "".join(traceback.format_exception(exception)).strip()


def test_manually_passed_exception_with_context_inside_except_block_has_correct_exception(
    capsys: pytest.CaptureFixture,
) -> None:
    log.LogConfig.configure_logging()
    try:
        raise Exception("error")
    except Exception as e:
        exception = e

    try:
        raise Exception("new error")
    except:
        log.exception("test", exception=exception)

    captured_log = json.loads(capsys.readouterr().out)
    assert captured_log["exception"].strip() == "".join(traceback.format_exception(exception)).strip()


def test_exception_within_except_block_has_correct_exception(capsys: pytest.CaptureFixture) -> None:
    log.LogConfig.configure_logging()
    try:
        raise Exception("error")
    except Exception as e:
        exception = e
        log.exception("test", exception=exception)
    captured_log = json.loads(capsys.readouterr().out)
    assert captured_log["exception"].strip() == "".join(traceback.format_exception(exception)).strip()
