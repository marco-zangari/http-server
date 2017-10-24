"""Tests for server and client modules."""

import pytest


@pytest.mark.parametrize('message', ['', 'M', 'Hello World!', 'aaaaaaab',
                                     'aaaaaaabaaaaaaab', 'éclair'])
def test_echo(message):
    """Test that message received from server is same as message sent."""
    from client import client
    assert client(message) == message
