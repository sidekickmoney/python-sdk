import json
import typing
import uuid

import boto3  # type: ignore
import pytest

from python_sdk import secrets


@pytest.fixture(scope="function")
def configure_aws_sm_secrets_engine(docker_compose: None) -> None:
    secrets.SecretsConfig.set_config_value(option="ENGINE", value="AWS_SM")
    secrets.SecretsConfig.set_config_value(option="ENGINE_AWS_SM_SECRET_KEY_ID", value="fake")
    secrets.SecretsConfig.set_config_value(option="ENGINE_AWS_SM_SECRET_ACCESS_KEY", value="fake")
    secrets.SecretsConfig.set_config_value(option="ENGINE_AWS_SM_SESSION_TOKEN", value="fake")
    secrets.SecretsConfig.set_config_value(option="ENGINE_AWS_SM_REGION_NAME", value="eu-west-1")
    secrets.SecretsConfig.set_config_value(option="ENGINE_AWS_SM_USE_SSL", value=False)
    secrets.SecretsConfig.set_config_value(option="ENGINE_AWS_SM_VERIFY", value=False)
    secrets.SecretsConfig.set_config_value(option="ENGINE_AWS_SM_ENDPOINT_URL", value="http://localhost:4566")


@pytest.fixture(scope="function")
def configure_aws_ps_secrets_engine(docker_compose: None) -> None:
    secrets.SecretsConfig.set_config_value(option="ENGINE", value="AWS_PS")
    secrets.SecretsConfig.set_config_value(option="ENGINE_AWS_PS_SECRET_KEY_ID", value="fake")
    secrets.SecretsConfig.set_config_value(option="ENGINE_AWS_PS_SECRET_ACCESS_KEY", value="fake")
    secrets.SecretsConfig.set_config_value(option="ENGINE_AWS_PS_SESSION_TOKEN", value="fake")
    secrets.SecretsConfig.set_config_value(option="ENGINE_AWS_PS_REGION_NAME", value="eu-west-1")
    secrets.SecretsConfig.set_config_value(option="ENGINE_AWS_PS_USE_SSL", value=False)
    secrets.SecretsConfig.set_config_value(option="ENGINE_AWS_PS_VERIFY", value=False)
    secrets.SecretsConfig.set_config_value(option="ENGINE_AWS_PS_ENDPOINT_URL", value="http://localhost:4566")


@pytest.fixture(scope="function")
def aws_sm_client(configure_aws_sm_secrets_engine: None) -> typing.Any:
    return boto3.client(
        service_name="secretsmanager",
        aws_access_key_id="fake",
        aws_secret_access_key="fake",
        aws_session_token="fake",
        region_name="eu-west-1",
        use_ssl=False,
        verify=False,
        endpoint_url="http://localhost:4566",
    )


@pytest.fixture(scope="function")
def aws_ps_client(configure_aws_ps_secrets_engine: None) -> typing.Any:
    return boto3.client(
        service_name="ssm",
        aws_access_key_id="fake",
        aws_secret_access_key="fake",
        aws_session_token="fake",
        region_name="eu-west-1",
        use_ssl=False,
        verify=False,
        endpoint_url="http://localhost:4566",
    )


@pytest.fixture(scope="function")
def random_aws_sm_secret_string(aws_sm_client: typing.Any) -> typing.Generator[tuple[str, str], None, None]:
    name, value = str(uuid.uuid4()), str(uuid.uuid4())
    response = aws_sm_client.create_secret(Name=name, SecretString=value)
    yield name, value
    aws_sm_client.delete_secret(SecretId=response["ARN"], RecoveryWindowInDays=0, ForceDeleteWithoutRecovery=True)


@pytest.fixture(scope="function")
def random_aws_sm_secret_binary(aws_sm_client: typing.Any) -> typing.Generator[tuple[str, str], None, None]:
    name, value = str(uuid.uuid4()), str(uuid.uuid4())
    response = aws_sm_client.create_secret(Name=name, SecretBinary=value.encode("utf-8"))
    yield name, value
    aws_sm_client.delete_secret(SecretId=response["ARN"], RecoveryWindowInDays=0, ForceDeleteWithoutRecovery=True)


@pytest.fixture(scope="function")
def random_aws_sm_secret_json(aws_sm_client: typing.Any) -> typing.Generator[tuple[str, dict[str, str]], None, None]:
    name, value = str(uuid.uuid4()), {str(uuid.uuid4()): str(uuid.uuid4())}
    response = aws_sm_client.create_secret(Name=name, SecretString=json.dumps(value))
    yield name, value
    aws_sm_client.delete_secret(SecretId=response["ARN"], RecoveryWindowInDays=0, ForceDeleteWithoutRecovery=True)


@pytest.fixture(scope="function")
def random_aws_ps_secret_string(aws_ps_client: typing.Any) -> typing.Generator[tuple[str, str], None, None]:
    name, value = str(uuid.uuid4()), str(uuid.uuid4())
    aws_ps_client.put_parameter(Name=name, Value=value, Type="String")
    yield name, value
    aws_ps_client.delete_parameter(Name=name)


@pytest.fixture(scope="function")
def random_aws_ps_secret_string_list(aws_ps_client: typing.Any) -> typing.Generator[tuple[str, list[str]], None, None]:
    name, value = str(uuid.uuid4()), [str(uuid.uuid4()), str(uuid.uuid4())]
    aws_ps_client.put_parameter(Name=name, Value=",".join(value), Type="StringList")
    yield name, value
    aws_ps_client.delete_parameter(Name=name)


@pytest.fixture(scope="function")
def random_aws_ps_secret_json(aws_ps_client: typing.Any) -> typing.Generator[tuple[str, dict[str, str]], None, None]:
    name, value = str(uuid.uuid4()), {str(uuid.uuid4()): str(uuid.uuid4())}
    aws_ps_client.put_parameter(Name=name, Value=json.dumps(value), Type="String")
    yield name, value
    aws_ps_client.delete_parameter(Name=name)
