import argparse
import subprocess
import sys
import typing

from .__version__ import __version__

_BLACK_BASE_PARAMETERS: typing.List[str] = ["black", ".", "--line-length", "120"]
_ISORT_BASE_PARAMETERS: typing.List[str] = [
    "isort",
    ".",
    "--force-single-line-imports",
    "--force-sort-within-sections",
]


def main() -> int:
    parser = _build_arg_parser()
    args = parser.parse_args()

    if args.command == "help":
        parser.print_help()
        exit_code = 0
    elif args.command == "version":
        exit_code = _show_version()
    elif args.command == "fmt":
        exit_code = _fmt(parser=args)
    else:
        parser.print_help()
        exit_code = 1

    return exit_code


def _show_version() -> int:
    print(__version__)
    return 0


def _build_arg_parser() -> argparse.ArgumentParser:
    # main parser
    main_parser = argparse.ArgumentParser(description="Python SDK", add_help=True)
    main_subparsers = main_parser.add_subparsers(title="Commands", dest="command")

    # help parser
    help_parser = main_subparsers.add_parser(description="Python SDK help", name="help", add_help=True)

    # version parser
    version_parser = main_subparsers.add_parser(description="Python SDK version", name="version", add_help=True)

    # fmt parser
    fmt_parser = main_subparsers.add_parser(description="Python SDK fmt", name="fmt", add_help=True)
    fmt_parser.add_argument(
        "--files", nargs="*", action="store", dest="files", required=True, help="One or more Python files to format."
    )
    fmt_parser.add_argument(
        "--ignore-files",
        dest="ignore_files",
        action="store_true",
        help="Files to ignore.",
    )
    fmt_parser.add_argument(
        "--check",
        action="store_true",
        dest="check",
        help="Checks if the files need to be formatted and prints them to the "
        "command line without modifying them. Returns 0 when nothing would change and "
        "returns 1 if the files require formatting.",
    )

    fmt_subparsers = fmt_parser.add_subparsers(title="Commands", dest="fmt_command")
    fmt_help_parser = fmt_subparsers.add_parser(description="Python SDK fmt help", name="help", add_help=True)

    return main_parser


def _fmt(parser: argparse.Namespace) -> int:
    if not _dependencies_available():
        print("Required dependencies not found. Did you 'pip install python-sdk[dev]' ?")
        sys.exit(1)

    black_exit_code = _black(files=parser.files, ignore_files=parser.ignore_files, check=parser.check)
    isort_exit_code = _isort(files=parser.files, ignore_files=parser.ignore_files, check=parser.check)

    return max([black_exit_code, isort_exit_code])


def _black(files: typing.List[str] = None, ignore_files: typing.List[str] = None, check: bool = False) -> int:
    args = []
    if check:
        args.append("--check")
    args = _BLACK_BASE_PARAMETERS + args

    result = subprocess.run(args)

    return result.returncode


def _isort(files: typing.List[str] = None, ignore_files: typing.List[str] = None, check: bool = False) -> int:
    args = []
    if check:
        args.append("--check")
    args = _ISORT_BASE_PARAMETERS + args

    result = subprocess.run(args)

    return result.returncode


def _dependencies_available():
    return _black_available() and _isort_available()


def _isort_available() -> bool:
    try:
        import isort

        return True
    except ImportError:
        return False


def _black_available() -> bool:
    try:
        import black

        return True
    except ImportError:
        return False


if __name__ == "__main__":
    _exit_code = main()
    sys.exit(_exit_code)
