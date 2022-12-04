import pathlib

_PACKAGED_VERSION_FILE = pathlib.Path(__file__).parent / "version"
_REPO_VERSION_FILE = pathlib.Path(__file__).parent.parent.parent / "version"

VERSION = _PACKAGED_VERSION_FILE.read_text() if _PACKAGED_VERSION_FILE.exists() else _REPO_VERSION_FILE.read_text()
