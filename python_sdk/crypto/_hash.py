import os
import sys

import argon2

from python_sdk import log

# TODO(lijok): can we implement this with cryptography to reduce number of deps?
# TODO(lijok): ensure values are of correct data type
# defaults are based on the RFC9106 high memory recommendation
# https://www.rfc-editor.org/rfc/rfc9106.html#name-parameter-choice
_TIME_COST: int = int(os.environ.get("PYTHON_SDK_HASH_TIME_COST", 1))
_MEMORY_COST: int = int(os.environ.get("PYTHON_SDK_HASH_MEMORY_COST_KIBIBYTES", 2097152))  # 2GB
_PARALLELISM: int = int(os.environ.get("PYTHON_SDK_HASH_PARALLELISM", 4))
_HASH_LENGTH: int = int(os.environ.get("PYTHON_SDK_HASH_HASH_LENGTH", 32))
_SALT_LENGTH: int = int(os.environ.get("PYTHON_SDK_HASH_SALT_LENGTH", 16))

log.info(
    "Hashing configured",
    TIME_COST=_TIME_COST,
    MEMORY_COST=_MEMORY_COST,
    PARALLELISM=_PARALLELISM,
    HASH_LENGTH=_HASH_LENGTH,
    SALT_LENGTH=_SALT_LENGTH,
    TYPE="Argon2id",
)

_HASHER = argon2.PasswordHasher(
    time_cost=_TIME_COST,
    memory_cost=_MEMORY_COST,
    parallelism=_PARALLELISM,
    hash_len=_HASH_LENGTH,
    salt_len=_SALT_LENGTH,
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
