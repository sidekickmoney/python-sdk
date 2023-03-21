import inspect
import json
import os
import pathlib
import sys

_VERSION_FILE_NAME: str = "version"


def version_file_based() -> str:
    if hasattr(sys, "_MEIPASS"):  # running as a pyinstaller frozen application
        packaged_version_file = pathlib.Path(getattr(sys, "_MEIPASS")) / _VERSION_FILE_NAME
        if not packaged_version_file.exists():
            raise FileNotFoundError(
                "Version lookup failed. "
                "Version file not found. "
                "We detected we're running in a PyInstaller frozen application. "
                f"Expected to find version file at: {packaged_version_file}."
            )

    calling_module_frame = inspect.stack()[1]
    calling_module_name = calling_module_frame[0]
    calling_module = inspect.getmodule(calling_module_name)
    if not calling_module or not calling_module.__file__:
        raise ModuleNotFoundError("Could not discover calling module.")
    calling_module_file = pathlib.Path(calling_module.__file__)

    current_dir = calling_module_file.parent
    checked = []
    while True:
        currently_checking = current_dir / _VERSION_FILE_NAME
        checked.append(currently_checking)

        if currently_checking.exists():
            return currently_checking.read_text().strip()

        if ".git" in os.listdir(current_dir):
            raise FileNotFoundError(
                "Version lookup failed. "
                "Version file not found. "
                "We traversed the filesystem until we hit the root of the repository. "
                f"Paths checked: {json.dumps(checked, indent=4, default=str)}"
            )

        if current_dir.parent == current_dir:
            raise FileNotFoundError(
                "Version lookup failed. "
                "Version file not found. "
                "We traversed the filesystem until we hit root of the filesystem. "
                f"Paths checked: {json.dumps(checked, indent=4, default=str)}"
            )

        current_dir = current_dir.parent
