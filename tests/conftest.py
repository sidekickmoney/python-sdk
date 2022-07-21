import logging


def pytest_sessionfinish() -> None:
    # Suppress logging errors after the session finishes.
    # Currently, pytest redirects sys.std* to its custom implementation for capsys etc.
    # This means, that our atexit handlers, which flush logs in the _log package, can end up attempting to write to a
    # closed file handle, if that filehandle is sys.std*, because, pytest will have closed it by the time atexit
    # handlers are run.
    # We are likely to rewrite the log stack at a later date to support hot config-reload, meaning, this will go away.
    logging.raiseExceptions = False
