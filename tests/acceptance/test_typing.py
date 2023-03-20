import subprocess


def test_typing() -> None:
    result = subprocess.run(["mypy", "."])
    assert result.returncode == 0
