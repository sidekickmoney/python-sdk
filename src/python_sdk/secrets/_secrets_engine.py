import typing

SecretValue: typing.TypeAlias = str | bytes | dict[str, typing.Any]


class SecretsEngine(typing.Protocol):
    def get_secret(self, secret_name: str) -> SecretValue:
        """
        Raises:
            SecretDoesNotExist: Requested secret does not exist.
            Unauthorized: Supplied credentials do not have the required permissions to access the requested secret.
        """
        ...
