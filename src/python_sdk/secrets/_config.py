import functools
import logging
import typing

from python_sdk import config
from python_sdk.secrets import _secrets_engine


# TODO(lijok): something to prevent this from being configured using secrets
# TODO(lijok): extract ENGINE_AWS_SM_BOTOCORE_CONFIG to top level
class Secrets(config.Config, option_prefix="PYTHON_SDK_SECRETS_"):
    ENGINE: typing.Literal["AWS_SM", "AWS_PM"] = config.Option(default="AWS_SM")
    ENGINE_AWS_SM_SECRET_KEY_ID: str | None = config.Option()
    ENGINE_AWS_SM_SECRET_ACCESS_KEY: str | None = config.Option()
    ENGINE_AWS_SM_SESSION_TOKEN: str | None = config.Option()
    ENGINE_AWS_SM_REGION_NAME: str | None = config.Option()
    ENGINE_AWS_SM_API_VERSION: str | None = config.Option()
    ENGINE_AWS_SM_USE_SSL: bool = config.Option(default=True)
    ENGINE_AWS_SM_VERIFY: bool = config.Option(default=True)
    ENGINE_AWS_SM_ENDPOINT_URL: str | None = config.Option()
    ENGINE_AWS_SM_BOTOCORE_CONFIG: config.UnvalidatedDict | None = config.Option(
        description="See https://botocore.amazonaws.com/v1/documentation/api/latest/reference/config.html"
    )

    @classmethod
    def post_load_hook(cls) -> None:
        cls.get_secrets_engine.cache_clear()

    @classmethod
    @functools.lru_cache(maxsize=1)
    def get_secrets_engine(cls) -> _secrets_engine.SecretsEngine:
        logging.debug(f"Using {cls.ENGINE} secrets engine for fetching secrets.")
        if cls.ENGINE == "AWS_SM":
            return cls._get_aws_sm_secrets_engine()

        raise NotImplementedError(f"Secrets engine not supported. engine={cls.ENGINE}")

    @classmethod
    def _get_aws_sm_secrets_engine(cls) -> _secrets_engine.SecretsEngine:
        from python_sdk.secrets import _aws_sm

        return _aws_sm.AWSSecretsManager(
            secret_key_id=cls.ENGINE_AWS_SM_SECRET_KEY_ID,
            secret_access_key=cls.ENGINE_AWS_SM_SECRET_ACCESS_KEY,
            session_token=cls.ENGINE_AWS_SM_SESSION_TOKEN,
            region_name=cls.ENGINE_AWS_SM_REGION_NAME,
            api_version=cls.ENGINE_AWS_SM_API_VERSION,
            use_ssl=cls.ENGINE_AWS_SM_USE_SSL,
            verify=cls.ENGINE_AWS_SM_VERIFY,
            endpoint_url=cls.ENGINE_AWS_SM_ENDPOINT_URL,
            botocore_config=cls.ENGINE_AWS_SM_BOTOCORE_CONFIG,
        )
