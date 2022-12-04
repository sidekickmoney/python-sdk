import os
import typing
import uuid

import boto3
import pytest


@pytest.fixture(scope="session", autouse=True)
def configuration() -> None:
    os.environ["PYTHON_SDK_SECRETS_ENGINE"] = "AWS_SM"
    os.environ["PYTHON_SDK_SECRETS_ENGINE_AWS_SM_SECRET_KEY_ID"] = "test"
    os.environ["PYTHON_SDK_SECRETS_ENGINE_AWS_SM_SECRET_ACCESS_KEY"] = "test"
    os.environ["PYTHON_SDK_SECRETS_ENGINE_AWS_SM_REGION_NAME"] = "us-east-1"
    os.environ["PYTHON_SDK_SECRETS_ENGINE_AWS_SM_VERIFY"] = "FALSE"
    os.environ["PYTHON_SDK_SECRETS_ENGINE_AWS_SM_ENDPOINT_URL"] = "http://localhost:4566"


@pytest.fixture(scope="function")
def random_aws_sm_secret() -> typing.Tuple[str, str]:
    client = boto3.client(
        service_name="secretsmanager",
        region_name="us-east-1",
        verify=False,
        endpoint_url="http://localhost:4566",
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )
    name = str(uuid.uuid4())
    value = str(uuid.uuid4())
    response = client.create_secret(Name=name, SecretString=value)
    yield name, value
    client.delete_secret(SecretId=response["ARN"], RecoveryWindowInDays=0, ForceDeleteWithoutRecovery=True)
