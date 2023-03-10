from python_sdk.secrets import _config
from python_sdk.secrets import _secrets_engine


def get_secret(secret_name: str) -> _secrets_engine.SecretValue:
    return _config.SecretsConfig.get_secrets_engine().get_secret(secret_name=secret_name)
