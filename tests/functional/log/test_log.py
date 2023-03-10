import inspect
import json

import pytest

from python_sdk import log

# TODO: Remove log.LogConfig.configure_logging() from all tests


@pytest.mark.parametrize("log_level", ["audit", "critical", "debug", "error", "info", "security", "warning"])
def test_log_works(capsys: pytest.CaptureFixture, log_level: str) -> None:
    log.LogConfig.configure_logging()
    log_method = getattr(log, log_level)
    log_method(f"test {log_level}")
    captured_log = json.loads(capsys.readouterr().out)
    assert captured_log["message"] == f"test {log_level}"


def test_log_message_is_correct(capsys: pytest.CaptureFixture) -> None:
    log.LogConfig.configure_logging()
    log.info("test")
    captured_log = json.loads(capsys.readouterr().out)
    assert captured_log["message"] == "test"


def test_log_level_is_uppercase(capsys: pytest.CaptureFixture) -> None:
    log.LogConfig.configure_logging()
    log.info("test")
    captured_log = json.loads(capsys.readouterr().out)
    assert captured_log["log_level"] == "INFO"


def test_log_function_name_is_correct(capsys: pytest.CaptureFixture) -> None:
    log.LogConfig.configure_logging()
    log.info("test")
    captured_log = json.loads(capsys.readouterr().out)
    assert captured_log["function_name"] == test_log_function_name_is_correct.__name__


def test_log_module_name_is_correct(capsys: pytest.CaptureFixture) -> None:
    log.LogConfig.configure_logging()
    log.info("test")
    captured_log = json.loads(capsys.readouterr().out)
    assert captured_log["module_name"] == __name__.split(".")[-1]


def test_log_module_path_is_correct(capsys: pytest.CaptureFixture) -> None:
    log.LogConfig.configure_logging()
    log.info("test")
    captured_log = json.loads(capsys.readouterr().out)
    assert captured_log["module_path"] == __file__


def test_log_line_number_is_correct(capsys: pytest.CaptureFixture) -> None:
    log.LogConfig.configure_logging()
    log.info("test")
    log_line_number = inspect.getframeinfo(inspect.currentframe()).lineno - 1
    captured_log = json.loads(capsys.readouterr().out)
    assert captured_log["line_number"] == log_line_number


# TODO: use freezegun
# def test_log_timestamp_is_correct(capsys: pytest.CaptureFixture) -> None:
#     log.LogConfig.configure_logging()
#     log.info("test")
#     captured_log = json.loads(capsys.readouterr().out)
#     assert captured_log["line_number"] == 51


# def test_log_timestamp_is_rfc3339_compliant(captured_log: dict[str, typing.Any]) -> None:
#     assert datetime.datetime.strptime(captured_log["timestamp"], '%Y-%m-%dT%H:%M:%S%z')
#     assert datetime.datetime.strptime(captured_log["timestamp"], '%Y-%m-%dT%H:%M:%S%z').tzinfo is not None
