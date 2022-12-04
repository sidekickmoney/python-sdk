import typing


def test_aws_sm_get_secret(random_aws_sm_secret: typing.Tuple[str, str]) -> None:
    from python_sdk import secrets

    name, value = random_aws_sm_secret
    response = secrets.get_secret(secret_name=name)
    assert response == value
