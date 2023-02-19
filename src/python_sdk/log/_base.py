import logging
import sys

from python_sdk.log import _formatters

# Set up a default logger, which can be used while the whole of python_sdk initializes.
_default_handler: logging.StreamHandler = logging.StreamHandler(stream=sys.stdout)
_default_handler.setFormatter(fmt=_formatters.StructuredLogMachineReadableFormatter())

_logger: logging.Logger = logging.getLogger()
_logger.setLevel("INFO")
for _existing_handler in _logger.handlers:
    _existing_handler.flush()
    _existing_handler.close()
    _logger.removeHandler(hdlr=_existing_handler)
_logger.addHandler(hdlr=_default_handler)
