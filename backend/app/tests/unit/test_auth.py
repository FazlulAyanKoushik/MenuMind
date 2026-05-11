import pytest
from app.core.security import hash_password, verify_password, create_access_token, decode_token


def test_password_hashing():
    pwd = "test_password_123"
    hashed = hash_password(pwd)
    assert hashed != pwd
    assert verify_password(pwd, hashed)
    assert not verify_password("wrong_password", hashed)


def test_access_token():
    data = {"sub": "user_123", "role": "consumer"}
    token = create_access_token(data)
    payload = decode_token(token)
    assert payload["sub"] == "user_123"
    assert payload["role"] == "consumer"
    assert payload["type"] == "access"
