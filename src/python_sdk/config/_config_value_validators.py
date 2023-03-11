import os
import pathlib
import typing

if typing.TYPE_CHECKING:
    from python_sdk.config import _config_option
    from python_sdk.config import _config_value_types


class ConfigValueValidationError(Exception):
    """Config Value does not pass validation."""

    ...


class ConfigValueValidator(typing.Protocol):
    name: str
    description: str

    def __call__(
        self,
        config_option_name: str,
        config_option: "_config_option.ConfigOption",
        config_value: typing.Any,
    ) -> None:
        """
        Raises:
            ConfigValueValidationError: Config value does not pass validation.
        """
        ...


class EnsureFileExists:
    name: str = "Ensure File Exists"
    description: str = "Validates that the file at a given path exists."

    def __call__(
        self,
        config_option_name: str,
        config_option: "_config_option.ConfigOption",
        config_value: pathlib.Path,
    ) -> None:
        """
        Raises:
            ConfigValueValidationError: Path does not exist or is not a directory.
        """
        if not config_value.exists():
            raise ConfigValueValidationError(f"File at {config_value} does not exist.")
        if not config_value.is_file():
            raise ConfigValueValidationError(f"{config_value} not a file.")


class EnsureDirectoryExists:
    name: str = "Ensure Directory Exists"
    description: str = "Validates that the directory at a given path exists."

    def __call__(
        self,
        config_option_name: str,
        config_option: "_config_option.ConfigOption",
        config_value: pathlib.Path,
    ) -> None:
        """
        Raises:
            ConfigValueValidationError: Path does not exist or is not a directory.
        """
        if not config_value.exists():
            raise ConfigValueValidationError(f"Directory at {config_value} does not exist.")
        if not config_value.is_dir():
            raise ConfigValueValidationError(f"{config_value} not a directory.")


class EnsurePathIsReadable:
    name: str = "Ensure Path is Readable"
    description: str = "Validates that a given path is readable."

    def __call__(
        self,
        config_option_name: str,
        config_option: "_config_option.ConfigOption",
        config_value: pathlib.Path,
    ) -> None:
        """
        Raises:
            ConfigValueValidationError: Path is not readable.
        """
        if not os.access(config_value, os.R_OK):
            raise ConfigValueValidationError(f"{config_value} is not readable.")


class EnsurePathIsWritable:
    name: str = "Ensure Path is Writable"
    description: str = "Validates that a given path is writeable."

    def __call__(
        self,
        config_option_name: str,
        config_option: "_config_option.ConfigOption",
        config_value: pathlib.Path,
    ) -> None:
        """
        Raises:
            ConfigValueValidationError: Path is not writeable.
        """
        if not os.access(config_value, os.W_OK):
            raise ConfigValueValidationError(f"{config_value} is not writeable")


class EnsurePathIsExecutable:
    name: str = "Ensure Path is Executable"
    description: str = "Validates that a given path is executable."

    def __call__(
        self,
        config_option_name: str,
        config_option: "_config_option.ConfigOption",
        config_value: pathlib.Path,
    ) -> None:
        """
        Raises:
            ConfigValueValidationError: Path is not executable.
        """
        if not os.access(config_value, os.EX_OK):
            # with contextlib.suppress(FileNotFoundError, PermissionError):
            #     os.chmod(config_value, os.stat(config_value).st_mode | stat.S_IEXEC)
            raise ConfigValueValidationError(f"{config_value} is not executable")


class EnsureFileType:
    name: str = "Ensure File Type"
    description: str = "Validates that the file at a given path is of set file type."

    def __init__(self, file_type: str) -> None:
        self.file_type = file_type if file_type[0] == "." else f".{file_type}"

    def __call__(
        self,
        config_option_name: str,
        config_option: "_config_option.ConfigOption",
        config_value: pathlib.Path,
    ) -> None:
        """
        Raises:
            ConfigValueValidationError: Path is not of correct file type.
        """
        if "".join(config_value.suffixes) != self.file_type:
            raise ConfigValueValidationError(f"{config_value} is not {self.file_type}")
