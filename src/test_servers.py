"""Tests for server and client modules."""
# -*- coding: utf-8 -*-

import pytest
import sys


@pytest.fixture(scope="session")
def fake_socket():
    """Set-up testing for HTTP respose structure."""
    if sys.version_info.major == 3:
        from io import BytesIO
    else:
        from StringIO import StringIO as BytesIO

    class FakeSocket(object):

        def __init__(self, response_str):
            self._file = BytesIO(response_str)

        def makefile(self, *args, **kwargs):
            return self._file

    return FakeSocket


@pytest.mark.parametrize('message', ['', 'M', 'Hello World!', 'aaaaaaab',
                                     'aaaaaaabaaaaaaab', 'éclair', 'This is a \
sentence longer than the others and has spaces too, with punctuation.'])
def test_success_on_sending_message(message):
    """Test that message received from server gets a 200 response."""
    from client import client
    assert client(message).split(b'\r\n')[0] == b'HTTP/1.1 200 OK'


def test_ok_response_well_formatted(fake_socket):
    """Test that formatting of 200 HTTP response is correct."""
    from server import response_ok
    from datetime import datetime as time

    if sys.version_info.major == 3:
        from http.client import HTTPResponse
    else:
        from httplib import HTTPResponse

    source = fake_socket(response_ok())
    response = HTTPResponse(source)
    response.begin()
    assert response.status == 200
    assert time.strptime(response.getheader('Date'),
                         '%a, %d %b %Y %H:%M:%S %Z')


def test_error_response_well_formatted(fake_socket):
    """Test that error reponse of 500 HTTP response is correct."""
    from server import response_error
    from datetime import datetime as time

    if sys.version_info.major == 3:
        from http.client import HTTPResponse
    else:
        from httplib import HTTPResponse

    source = fake_socket(response_error())
    response = HTTPResponse(source)
    response.begin()
    assert response.status == 500
    assert time.strptime(response.getheader('Date'),
                         '%a, %d %b %Y %H:%M:%S %Z')

"""
https://stackoverflow.com/questions/24728088/python-parse-http-response-string
Answer by Jeremy Allen
Written in Python 2
# for python 2
from httplib import HTTPResponse
from StringIO import StringIO
# for python 3
from http.client import HTTPResponse
from io import BytesIO

http_response_str = "HTTP/1.1 200 OK
Date: Thu, Jul  3 15:27:54 2014
Content-Type: text/xml; charset="utf-8"
Connection: close
Content-Length: 626"

class FakeSocket():
    def __init__(self, response_str):
        self._file = StringIO(response_str)
    def makefile(self, *args, **kwargs):
        return self._file

source = FakeSocket(http_response_str)
response = HTTPResponse(source)
response.begin()
print "status:", response.status
print "single header:", response.getheader('Content-Type')
print "content:", response.read(len(http_response_str))
# the len here will give a 'big enough' value to read the whole content
"""
