import hypothesis
from hypothesis import strategies

from python_sdk import crypto


@hypothesis.settings(deadline=None)
@hypothesis.given(password=strategies.text(min_size=1))
def test_hash_password_password_matches_hash_roundtrip(password: str) -> None:
    hashed_password = crypto.hash_password(password=password)
    assert crypto.password_matches_hash(password=password, hash=hashed_password)
