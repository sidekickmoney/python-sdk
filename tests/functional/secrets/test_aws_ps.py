import json

from python_sdk import secrets


def test_aws_ps_get_secret_string(random_aws_ps_secret_string: tuple[str, str]) -> None:
    name, value = random_aws_ps_secret_string
    assert secrets.get_secret_value(key=name).read().decode("utf-8") == value


def test_aws_ps_get_secret_string_list(random_aws_ps_secret_string_list: tuple[str, str]) -> None:
    name, value = random_aws_ps_secret_string_list
    assert secrets.get_secret_value(key=name).read().decode("utf-8").split(",") == value


def test_aws_ps_get_secret_string_json(random_aws_ps_secret_json: tuple[str, str]) -> None:
    name, value = random_aws_ps_secret_json
    assert json.loads(secrets.get_secret_value(key=name).read().decode("utf-8")) == value
