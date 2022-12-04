import subprocess


def test_python_code_is_formatted() -> None:
    result = subprocess.run(["black", "--line-length", "120", "--check", "."])
    assert result.returncode == 0
    result = subprocess.run(
        [
            "isort",
            "--line-length",
            "120",
            "--force-single-line-imports",
            "--force-sort-within-sections",
            "--profile",
            "black",
            "--check",
            ".",
        ]
    )
    assert result.returncode == 0
