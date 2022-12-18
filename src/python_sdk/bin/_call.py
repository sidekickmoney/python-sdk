import dataclasses
import functools
import os
import pathlib
import subprocess
import typing

from python_sdk import log
from python_sdk import utils


class Stringable(typing.Protocol):
    def __str__(self) -> str:
        ...


@dataclasses.dataclass
class BinaryNotInstalled(FileNotFoundError):
    binary: str

    def __str__(self) -> str:
        return self.binary


@dataclasses.dataclass
class CalledProcessError(Exception):
    output: str
    exit_code: int

    def __str__(self) -> str:
        return f"{self.exit_code}\n{self.output}"


def call(
    *args: Stringable,
    binary: str | pathlib.Path,
    sudo: bool = False,
    sudo_binary: str = "sudo",
    environment_variables: dict[str, str] | None = None,
    stream_output: bool = False,
    stream_printer: typing.Callable[[str], None] = functools.partial(print, end="", flush=True),
    force_arch: typing.Literal["amd64", "x86_64"] | None = None,
) -> str:
    """
    Raises:
        BinaryNotInstalled: binary not installed
    """
    env = environment_variables if environment_variables is not None else dict(os.environ)

    try:
        binary_full_path = utils.which(binary)
        sudo_full_path = utils.which(sudo_binary)
    except FileNotFoundError as e:
        raise BinaryNotInstalled(binary=e.filename) from e

    command = [binary_full_path] + [str(i) for i in args]
    if sudo:
        command.insert(0, sudo_full_path)
    if force_arch:
        command.insert(0, "arch")
        command.insert(1, f"-{force_arch}")

    log.info("Calling command", binary=binary_full_path, command=command)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)

    output = ""
    for line in iter(process.stdout.readline, ""):  # type: ignore
        output += line
        if stream_output:
            stream_printer(line)

    log.debug(
        "Called command output", binary=binary_full_path, command=command, output=output, exit_code=process.returncode
    )

    process.wait()

    if process.returncode:
        raise CalledProcessError(output=output, exit_code=process.returncode)

    return output.strip()
