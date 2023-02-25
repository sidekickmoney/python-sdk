from python_sdk import secrets


def test_aws_ps_get_secret_string(random_aws_ps_secret_string: tuple[str, str]) -> None:
    name, value = random_aws_ps_secret_string
    assert secrets.get_secret(secret_name=name) == value


def test_aws_ps_get_secret_string_list(random_aws_ps_secret_string_list: tuple[str, str]) -> None:
    name, value = random_aws_ps_secret_string_list
    assert secrets.get_secret(secret_name=name) == value


def test_aws_ps_get_secret_string_json(random_aws_ps_secret_json: tuple[str, str]) -> None:
    name, value = random_aws_ps_secret_json
    assert secrets.get_secret(secret_name=name) == value
