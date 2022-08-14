import subprocess


def test_python_code_is_formatted() -> None:
    result = subprocess.run(["python-sdk", "fmt", "--files", "."])
    assert result.returncode == 0, result.stdout
