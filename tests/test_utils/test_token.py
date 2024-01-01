import time

from flaskr.util import token


def test_token_create(test_client):
    token_dump = token.generate_token("test@email.com")
    assert token_dump


def test_token_verify_valid(test_client):
    token_dump = token.generate_token("test@email.com")
    start_value = token.verify_token(token_dump)

    assert start_value


def test_token_verify_invalid(test_client):
    token_dump = token.generate_token("test@email.com")
    start_value = token.verify_token("nonce value")

    assert not start_value


def test_token_verify_time_expired(test_client):
    token_dump = token.generate_token("test@email.com")
    time.sleep(2)
    start_value = token.verify_token(token_dump, max_age=1)

    assert not start_value
