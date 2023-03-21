import inspect
import json
import os
import pathlib


# TODO: Add debug logs
def version_file_based(version_file_name: str = "version") -> str:
    # TODO: In manual testing, this appears to not be required. Will need to add automated tests.
    # if hasattr(sys, "_MEIPASS"):  # Running as a PyInstaller frozen application
    #     packaged_version_file = pathlib.Path(getattr(sys, "_MEIPASS")) / version_file_name
    #     if not packaged_version_file.exists():
    #         raise FileNotFoundError(
    #             "Version lookup failed. "
    #             "Version file not found. "
    #             "We detected we're running in a PyInstaller frozen application. "
    #             f"Expected to find version file at: {packaged_version_file}."
    #         )
    #     return packaged_version_file.read_text()

    calling_module_frame = inspect.stack()[1]
    calling_module_name = calling_module_frame[0]
    calling_module = inspect.getmodule(calling_module_name)
    if not calling_module or not calling_module.__file__:
        raise ModuleNotFoundError("Could not discover calling module.")
    calling_module_file = pathlib.Path(calling_module.__file__)

    current_dir = calling_module_file.parent
    checked = []
    while True:
        currently_checking = current_dir / version_file_name
        checked.append(currently_checking)

        if currently_checking.exists():
            return currently_checking.read_text().strip()

        # current_dir might not exist in PyInstaller frozen applications.
        if current_dir.exists() and ".git" in os.listdir(current_dir):
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
