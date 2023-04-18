import dataclasses
import functools
import logging
import os
import pathlib
import subprocess
import typing

from python_sdk import utils


@dataclasses.dataclass
class BinaryNotInstalled(FileNotFoundError):
    binary: str

    def __str__(self) -> str:
        return self.binary


class CalledProcessError(Exception):
    def __init__(self, message: str, output: str, exit_code: int) -> None:
        super().__init__(message, output, exit_code)
        self.output = output
        self.exit_code = exit_code

    def __str__(self) -> str:
        return f"{self.exit_code}\n{self.output}"


def call(
    *args: typing.Any,
    sudo: bool = False,
    sudo_binary: str = "sudo",
    environment_variables: dict[str, str] | None = None,
    stream_output: bool = False,
    stream_printer: typing.Callable[[str], None] = functools.partial(print, end="", flush=True),
    force_arch: typing.Literal["amd64", "x86_64"] | None = None,
    stdin: typing.TextIO | None = None,
) -> str:
    """
    Raises:
        BinaryNotInstalled: binary not installed
    """
    env = environment_variables if environment_variables is not None else dict(os.environ)

    binary: str = args[0]
    arguments: typing.Any = [str(argument) for argument in args[1:]]

    try:
        binary_full_path = utils.which(binary)
        sudo_full_path = utils.which(sudo_binary)
    except FileNotFoundError as e:
        raise BinaryNotInstalled(binary=e.filename) from e

    command: list[str | pathlib.Path] = [binary_full_path] + arguments
    if sudo:
        command.insert(0, sudo_full_path)
    if force_arch:
        command.insert(0, "arch")
        command.insert(1, f"-{force_arch}")

    logging.debug(f"Calling command. binary={binary_full_path} {command=}")
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=stdin, text=True, env=env
    )

    output = ""
    for line in iter(process.stdout.readline, ""):  # type: ignore
        output += line
        if stream_output:
            stream_printer(line)

    logging.debug(
        f"Called command output. binary={binary_full_path} {command=} {output=} exit_code={process.returncode}"
    )

    process.wait()

    if process.returncode:
        raise CalledProcessError("Called process failure.", output=output, exit_code=process.returncode)

    return output.strip()
