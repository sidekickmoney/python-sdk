import subprocess
import typing

import pytest

from tests.functional.log_fixtures import *
from tests.functional.secrets_fixtures import *


@pytest.fixture(scope="session", autouse=False)
def docker_compose() -> typing.Generator[None, None, None]:
    subprocess.check_call(["docker", "compose", "up", "--build", "--wait"])
    yield
    subprocess.check_call(["docker", "compose", "down"])
