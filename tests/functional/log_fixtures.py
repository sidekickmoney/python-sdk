import json
import typing

import pytest

from python_sdk import log


@pytest.fixture(scope="function", autouse=True)
def configure_logging() -> None:
    # TODO: Figure this out
    # https://github.com/pytest-dev/pytest/issues/5502#issuecomment-647157873
    import logging

    loggers = [logging.getLogger()] + list(logging.Logger.manager.loggerDict.values())
    for logger in loggers:
        handlers = getattr(logger, "handlers", [])
        for handler in handlers:
            logger.removeHandler(handler)  # type: ignore

    log.LogConfig.configure_logging()
    log.LogConfig.set_config_value(option="LEVEL", value="DEBUG")


@pytest.fixture(scope="function")
def captured_log(capsys: pytest.CaptureFixture[str]) -> dict[str, typing.Any]:
    log.LogConfig.configure_logging()
    log.info("test")
    return dict(json.loads(capsys.readouterr().out))
