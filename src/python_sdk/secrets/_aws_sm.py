import dataclasses
import json
import typing

import boto3

from python_sdk import _log

from . import _exceptions


@dataclasses.dataclass
class AWSSecretsManager:
    secret_key_id: str
    secret_access_key: str
    region_name: str
    session_token: typing.Optional[str] = None
    api_version: typing.Optional[str] = None
    use_ssl: bool = True
    verify: bool = True
    endpoint_url: str = ""

    @property
    def _client(self) -> typing.Any:
        client = getattr(self, "client", None)
        if not client:
            client = boto3.client(
                service_name="secretsmanager",
                region_name=self.region_name,
                api_version=self.api_version,
                use_ssl=self.use_ssl,
                verify=self.verify,
                endpoint_url=self.endpoint_url or None,
                aws_access_key_id=self.secret_key_id,
                aws_secret_access_key=self.secret_access_key,
                aws_session_token=self.session_token,
            )
            setattr(self, "client", client)
        return client

    def get_secret(self, secret_name: str) -> str:
        _log.debug("Getting secret", secret_name=secret_name)
        try:
            response = self._client.get_secret_value(SecretId=secret_name)
        except Exception as e:
            raise _exceptions.SecretDoesNotExist() from e  # TODO
        if response["SecretString"]:
            try:
                secret = json.loads(response["SecretString"])
            except json.JSONDecodeError:
                secret = response["SecretString"]
        else:
            secret = response["SecretBinary"]
        return secret
