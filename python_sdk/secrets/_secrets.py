import typing

from python_sdk import _log
from python_sdk import config


# TODO(lijok): something to prevent this from being configured using secrets
@config.config(prefix="PYTHON_SDK_")
class _Config:
    SECRETS_ENGINE: typing.Literal["AWS_SM"]
    SECRETS_ENGINE_AWS_SM_SECRET_KEY_ID: typing.Optional[str]
    SECRETS_ENGINE_AWS_SM_SECRET_ACCESS_KEY: typing.Optional[str]
    SECRETS_ENGINE_AWS_SM_SESSION_TOKEN: typing.Optional[str]
    SECRETS_ENGINE_AWS_SM_REGION_NAME: typing.Optional[str]
    SECRETS_ENGINE_AWS_SM_API_VERSION: typing.Optional[str]
    SECRETS_ENGINE_AWS_SM_USE_SSL: str = True
    SECRETS_ENGINE_AWS_SM_VERIFY: str = True
    SECRETS_ENGINE_AWS_SM_ENDPOINT_URL: typing.Optional[str]


class _SecretsEngine(typing.Protocol):
    def __init__(self, **kwargs) -> None:
        ...

    def get_secret(self, secret_name: str) -> str:
        ...


def _get_secrets_engine() -> _SecretsEngine:
    if _Config.SECRETS_ENGINE == "AWS_SM":
        _log.info(f"Using {_Config.SECRETS_ENGINE} secrets engine for fetching secrets")

        from ._aws_sm import AWSSecretsManager

        return AWSSecretsManager(
            secret_key_id=_Config.SECRETS_ENGINE_AWS_SM_SECRET_KEY_ID,
            secret_access_key=_Config.SECRETS_ENGINE_AWS_SM_SECRET_ACCESS_KEY,
            session_token=_Config.SECRETS_ENGINE_AWS_SM_SESSION_TOKEN,
            region_name=_Config.SECRETS_ENGINE_AWS_SM_REGION_NAME,
            api_version=_Config.SECRETS_ENGINE_AWS_SM_API_VERSION,
            use_ssl=_Config.SECRETS_ENGINE_AWS_SM_USE_SSL,
            verify=_Config.SECRETS_ENGINE_AWS_SM_VERIFY,
            endpoint_url=_Config.SECRETS_ENGINE_AWS_SM_ENDPOINT_URL,
        )
    else:
        # should never happen
        raise AssertionError(f"Secrets engine {_Config.SECRETS_ENGINE} not supported")


try:
    _SECRETS_ENGINE = _get_secrets_engine()
except Exception as e:
    _log.exception(e)
    raise

get_secret = _SECRETS_ENGINE.get_secret
