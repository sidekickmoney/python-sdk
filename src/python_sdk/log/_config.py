import logging
import logging.handlers
import multiprocessing
import sys
import typing

from python_sdk import config
from python_sdk.log import _formatters


class LogConfig(config.Config, option_prefix="PYTHON_SDK_LOG_"):
    LEVEL: typing.Literal["DEBUG", "INFO", "SECURITY", "AUDIT", "WARNING", "ERROR", "CRITICAL"] = config.Option(
        default="INFO"
    )
    OUTPUT_STYLE: typing.Literal["MACHINE_READABLE", "HUMAN_READABLE"] = config.Option(default="MACHINE_READABLE")
    DESTINATION: typing.Literal["STDOUT", "STDERR", "ROTATING_FILE"] = config.Option(default="STDOUT")
    DESTINATION_ROTATING_FILE_PATH: str | None = config.Option(validators=[config.EnsurePathIsWritable()])
    DESTINATION_ROTATING_FILE_MAX_SIZE_BYTES: int = config.Option(default=1073741824)
    DESTINATION_ROTATING_FILE_MAX_NUMBER_OF_FILES: int = config.Option(default=10)
    INCLUDE_LOG_FILENAME: bool = config.Option(default=False)
    INCLUDE_FUNCTION_NAME: bool = config.Option(default=True)
    INCLUDE_LINE_NUMBER: bool = config.Option(default=True)
    INCLUDE_MODULE_NAME: bool = config.Option(default=True)
    INCLUDE_MODULE_PATH: bool = config.Option(default=True)
    INCLUDE_PROCESS_ID: bool = config.Option(default=False)
    INCLUDE_PROCESS_NAME: bool = config.Option(default=False)
    INCLUDE_THREAD_ID: bool = config.Option(default=False)
    INCLUDE_THREAD_NAME: bool = config.Option(default=False)
    INCLUDE_PYTHON_SDK_VERSION: bool = config.Option(default=False)

    @classmethod
    def post_load_hook(cls) -> None:
        cls.configure_logging()

    @classmethod
    def configure_logging(cls) -> None:
        # now that we have a config, set up a logger as dictated by the config
        logger = logging.getLogger()

        logger.setLevel(level=cls.LEVEL)

        for existing_handler in logger.handlers:
            existing_handler.flush()
            existing_handler.close()
            logger.removeHandler(hdlr=existing_handler)

        logger.addHandler(hdlr=cls.handler())

    @classmethod
    def formatter(cls) -> _formatters.StructuredLogFormatter:
        formatters = {
            "HUMAN_READABLE": _formatters.StructuredLogHumanReadableFormatter,
            "MACHINE_READABLE": _formatters.StructuredLogMachineReadableFormatter,
        }
        formatter = formatters[cls.OUTPUT_STYLE]
        return formatter(
            include_current_log_filename=cls.INCLUDE_LOG_FILENAME,
            include_function_name=cls.INCLUDE_FUNCTION_NAME,
            include_line_number=cls.INCLUDE_LINE_NUMBER,
            include_module_name=cls.INCLUDE_MODULE_NAME,
            include_module_path=cls.INCLUDE_MODULE_PATH,
            include_process_id=cls.INCLUDE_PROCESS_ID,
            include_process_name=cls.INCLUDE_PROCESS_NAME,
            include_thread_id=cls.INCLUDE_THREAD_ID,
            include_thread_name=cls.INCLUDE_THREAD_NAME,
            include_python_sdk_version=cls.INCLUDE_PYTHON_SDK_VERSION,
        )

    @classmethod
    def handler(cls) -> logging.Handler:
        handler: logging.Handler

        if cls.DESTINATION == "STDOUT":
            handler = logging.StreamHandler(stream=sys.stdout)
            handler.setFormatter(fmt=cls.formatter())
        elif cls.DESTINATION == "STDERR":
            handler = logging.StreamHandler(stream=sys.stderr)
            handler.setFormatter(fmt=cls.formatter())
        elif cls.DESTINATION == "ROTATING_FILE":
            assert cls.DESTINATION_ROTATING_FILE_PATH is not None
            rotating_file_handler = logging.handlers.RotatingFileHandler(
                filename=cls.DESTINATION_ROTATING_FILE_PATH,
                maxBytes=cls.DESTINATION_ROTATING_FILE_MAX_SIZE_BYTES,
                backupCount=cls.DESTINATION_ROTATING_FILE_MAX_NUMBER_OF_FILES,
                encoding="utf-8",
            )
            rotating_file_handler.setFormatter(fmt=cls.formatter())
            queue: multiprocessing.Queue[logging.LogRecord] = multiprocessing.Queue(-1)
            handler = logging.handlers.QueueHandler(queue=queue)
            queue_listener = logging.handlers.QueueListener(queue, rotating_file_handler, respect_handler_level=True)
            queue_listener.start()
        else:
            raise NotImplementedError(f"{cls.DESTINATION} not supported.")

        return handler
