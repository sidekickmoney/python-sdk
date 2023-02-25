import contextlib
import json
import logging
import typing

import boto3
import botocore.exceptions

from python_sdk.secrets import _exceptions
from python_sdk.secrets import _secrets_engine


# Boto3 does not have types, so we have to make our own.
class AWSSecretsManagerClient(typing.Protocol):
    def get_secret_value(self, **kwargs: dict[str, typing.Any]) -> dict[str, typing.Any]:
        ...


class AWSSecretsManager(_secrets_engine.SecretsEngine):
    client: AWSSecretsManagerClient

    def __init__(
        self,
        secret_key_id: str | None = None,
        secret_access_key: str | None = None,
        session_token: str | None = None,
        region_name: str | None = None,
        api_version: str | None = None,
        use_ssl: bool = True,
        verify: bool = True,
        endpoint_url: str | None = None,
        botocore_config: dict[str, str] | None = None,
    ) -> None:
        self.client = boto3.client(
            service_name="secretsmanager",
            aws_access_key_id=secret_key_id,
            aws_secret_access_key=secret_access_key,
            aws_session_token=session_token,
            region_name=region_name,
            api_version=api_version,
            use_ssl=use_ssl,
            verify=verify,
            endpoint_url=endpoint_url,
            config=botocore_config,
        )

    def get_secret(self, secret_name: str) -> _secrets_engine.SecretValue:
        logging.debug(f"Getting secret. {secret_name=}")
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                raise _exceptions.SecretDoesNotExist(e.response["Error"]["Message"]) from e
            elif e.response["Error"]["Code"] == "NotAuthorizedException":
                raise _exceptions.Unauthorized(e.response["Error"]["Message"]) from e
            raise

        if "SecretBinary" in response:
            secret = response["SecretBinary"].decode("utf-8")
        else:
            secret = response["SecretString"]

        with contextlib.suppress(json.JSONDecodeError):
            secret = json.loads(secret)

        return secret
