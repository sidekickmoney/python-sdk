import typing

from python_sdk import _log
from python_sdk import config


# TODO(lijok): something to prevent this from being configured using secrets
@config.config(prefix="PYTHON_SDK_SECRETS_")
class _Config:
    ENGINE: typing.Literal["AWS_SM"]
    ENGINE_AWS_SM_SECRET_KEY_ID: typing.Optional[str]
    ENGINE_AWS_SM_SECRET_ACCESS_KEY: typing.Optional[str]
    ENGINE_AWS_SM_SESSION_TOKEN: typing.Optional[str]
    ENGINE_AWS_SM_REGION_NAME: typing.Optional[str]
    ENGINE_AWS_SM_API_VERSION: typing.Optional[str]
    ENGINE_AWS_SM_USE_SSL: bool = True
    ENGINE_AWS_SM_VERIFY: bool = True
    ENGINE_AWS_SM_ENDPOINT_URL: typing.Optional[str]


class _SecretsEngine(typing.Protocol):
    def __init__(self, **kwargs: typing.Dict[str, typing.Any]) -> None:
        ...

    def get_secret(self, secret_name: str) -> str:
        ...


def _get_secrets_engine() -> _SecretsEngine:
    if _Config.ENGINE == "AWS_SM":
        _log.debug(f"Using {_Config.ENGINE} secrets engine for fetching secrets")

        from ._aws_sm import AWSSecretsManager

        return AWSSecretsManager(
            secret_key_id=_Config.ENGINE_AWS_SM_SECRET_KEY_ID,
            secret_access_key=_Config.ENGINE_AWS_SM_SECRET_ACCESS_KEY,
            session_token=_Config.ENGINE_AWS_SM_SESSION_TOKEN,
            region_name=_Config.ENGINE_AWS_SM_REGION_NAME,
            api_version=_Config.ENGINE_AWS_SM_API_VERSION,
            use_ssl=_Config.ENGINE_AWS_SM_USE_SSL,
            verify=_Config.ENGINE_AWS_SM_VERIFY,
            endpoint_url=_Config.ENGINE_AWS_SM_ENDPOINT_URL,
        )

    raise ValueError(f"Secrets engine not supported: {_Config.ENGINE}")  # should never happen


try:
    _SECRETS_ENGINE = _get_secrets_engine()
except Exception as e:
    _log.exception(e)
    raise

get_secret = _SECRETS_ENGINE.get_secret
