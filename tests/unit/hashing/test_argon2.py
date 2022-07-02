from python_sdk import hashing


def test_hash_password_password_matches_hash_roundtrip() -> None:
    password = "hunter2"
    hashed_password = hashing.hash_password(password=password)
    assert hashing.password_matches_hash(password=password, hash=hashed_password)
