"""Tests for server and client modules."""
# -*- coding: utf-8 -*-

import pytest


@pytest.mark.parametrize('message', ['', 'M', 'Hello World!', 'aaaaaaab',
                                     'aaaaaaabaaaaaaab', 'éclair', 'This is the \
                                     sentence that is longer than the others \
                                     and has spaces too, with punctuation.'])
def test_echo(message):
    """Test that message received from server is same as message sent."""
    from client import client
    assert client(message) == message
