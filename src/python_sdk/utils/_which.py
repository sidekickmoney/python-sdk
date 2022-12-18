import os
import pathlib
import shutil


def which(cmd: str | pathlib.Path, mode: int = os.F_OK | os.X_OK, path: str | None = None) -> pathlib.Path:
    """
    Raises:
        FileNotFoundError: executable not found
    """

    if result := shutil.which(cmd=cmd, mode=mode, path=path):
        return pathlib.Path(result)
    else:
        raise FileNotFoundError(cmd)
