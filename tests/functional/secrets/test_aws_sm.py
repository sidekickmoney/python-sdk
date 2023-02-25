from python_sdk import secrets


def test_aws_sm_get_secret_string(random_aws_sm_secret_string: tuple[str, str]) -> None:
    name, value = random_aws_sm_secret_string
    assert secrets.get_secret(secret_name=name) == value


def test_aws_sm_get_secret_binary(random_aws_sm_secret_binary: tuple[str, bytes]) -> None:
    name, value = random_aws_sm_secret_binary
    assert secrets.get_secret(secret_name=name) == value


def test_aws_sm_get_secret_json(random_aws_sm_secret_json: tuple[str, bytes]) -> None:
    name, value = random_aws_sm_secret_json
    assert secrets.get_secret(secret_name=name) == value
