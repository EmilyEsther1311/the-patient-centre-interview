from datetime import datetime, timedelta
import pytest

from analytics_buffer import AnalyticsBuffer
from mock_api import MockApi

def test_invalid_buffer_limit_raises_error():
    api = MockApi(1)
    with pytest.raises(TypeError):
        AnalyticsBuffer("Hello", 10, api, 5)
    with pytest.raises(ValueError):
        AnalyticsBuffer(0, 10, api, 5)

def test_invalid_timer_limit_raises_error():
    api = MockApi(1)
    with pytest.raises(TypeError):
        AnalyticsBuffer(3, "Hello", api, 5)
    with pytest.raises(ValueError):
        AnalyticsBuffer(3, 0, api, 5)

def test_invalid_api_raises_error():
    with pytest.raises(TypeError):
        AnalyticsBuffer(3, 3, "api", 5)

def test_invalid_failure_limit_raises_error():
    api = MockApi(1)
    with pytest.raises(TypeError):
        AnalyticsBuffer(3, 3, api, "Hello")
    with pytest.raises(ValueError):
        AnalyticsBuffer(3, 3, api, 0)

def test_does_not_flush_before_buffer_limit():
    api = MockApi(1) #Always successful API
    buffer = AnalyticsBuffer(3, 10, api, 5)

    buffer.track("event1")
    buffer.track("event2")

    assert len(buffer.buffer) == 2


def test_flushes_when_buffer_limit_is_reached():
    api = MockApi(1) #Always successful API
    buffer = AnalyticsBuffer(3, 10, api,5)

    buffer.track("event1")
    buffer.track("event2")
    buffer.track("event3")

    assert len(buffer.buffer) == 0


def test_flushes_when_timer_expires():
    api = MockApi(1)  # Always successful API
    buffer = AnalyticsBuffer(10,5,api,5)

    buffer.lastCall = datetime.now() - timedelta(seconds=6)
    buffer.track("event")

    assert len(buffer.buffer) == 0


def test_failed_api_call_does_not_clear_buffer():
    api = MockApi(0)  # Always unsuccessful API
    buffer = AnalyticsBuffer(2,10, api,5)

    buffer.track("event1")
    buffer.track("event2")

    assert len(buffer.buffer) == 2
    assert buffer.failureCount == 1


def test_failure_limit_raises_runtime_error():
    api = MockApi(0)  # Always unsuccessful API
    buffer = AnalyticsBuffer(1,10, api,2)

    buffer.track("event1")

    with pytest.raises(RuntimeError):
        buffer.track("event2")

def test_empty_buffer_does_not_cause_flush():
    api = MockApi(0)  # Always unsuccessful API
    buffer = AnalyticsBuffer(5,10, api,10)

    #Timer initiates flush but buffer is empty
    buffer.lastCall = datetime.now() - timedelta(seconds=6)
    buffer.track()

    #Flush occurred -> `failureCount = 1`, since API unsuccessful
    assert buffer.failureCount == 0