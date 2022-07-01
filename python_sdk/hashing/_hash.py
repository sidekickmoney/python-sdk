import argon2

from python_sdk import _log
from python_sdk import config


# defaults are based on the RFC9106 high memory recommendation
# https://www.rfc-editor.org/rfc/rfc9106.html#name-parameter-choice
@config.config(prefix="PYTHON_SDK_")
class _Config:
    HASH_TIME_COST: int = 1
    HASH_MEMORY_COST_KIBIBYTES: int = 2097152  # 2GB
    HASH_PARALLELISM: int = 4
    HASH_HASH_LENGTH: int = 32
    HASH_SALT_LENGTH: int = 16


_log.info(
    "Hashing configured",
    TIME_COST=_Config.HASH_TIME_COST,
    MEMORY_COST=_Config.HASH_MEMORY_COST_KIBIBYTES,
    PARALLELISM=_Config.HASH_PARALLELISM,
    HASH_LENGTH=_Config.HASH_HASH_LENGTH,
    SALT_LENGTH=_Config.HASH_SALT_LENGTH,
    TYPE="Argon2id",
)

_HASHER = argon2.PasswordHasher(
    time_cost=_Config.HASH_TIME_COST,
    memory_cost=_Config.HASH_MEMORY_COST_KIBIBYTES,
    parallelism=_Config.HASH_PARALLELISM,
    hash_len=_Config.HASH_HASH_LENGTH,
    salt_len=_Config.HASH_SALT_LENGTH,
    encoding="utf-8",
    type=argon2.Type.ID,
)


def hash_password(password: str) -> str:
    return _HASHER.hash(password=password)


def password_matches_hash(password: str, hash: str) -> bool:
    # This looks a bit weird because .verify returns True if the hash matches, and raises an exception if it doesn't.
    # We want to return a bool either way, so we wrap it in a try except.
    try:
        matches = _HASHER.verify(hash=hash, password=password)
    except argon2.exceptions.VerifyMismatchError:
        matches = False
    return matches


def needs_rehash(hash: str) -> bool:
    return _HASHER.check_needs_rehash(hash=hash)
