import pytest
from mock_api import MockApi


def test_success_rate_must_be_between_zero_and_one():
    with pytest.raises(ValueError):
        MockApi(1.1)

def test_success_rate_must_be_between_an_integer_or_float():
    with pytest.raises(TypeError):
        MockApi("Hello")

def test_api_call_always_succeeds_when_success_rate_is_one():
    count = 0
    api = MockApi(1)

    for i in range(1000):
        count += (1-api.call())

    assert count == 0


def test_api_call_always_fails_when_success_rate_is_zero():
    count = 0
    api = MockApi(0)

    for i in range(1000):
        count += api.call()

    assert count == 0


