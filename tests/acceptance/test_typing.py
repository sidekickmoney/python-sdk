import subprocess

import pytest


@pytest.mark.skip("TODO")
def test_typing() -> None:
    result = subprocess.run(["mypy", "."])
    assert result.returncode == 0
