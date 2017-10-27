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


def test_error_response_500_well_formatted(fake_socket):
    """Test that error reponse of 500 HTTP response is correct."""
    from server import response_error
    from datetime import datetime as time

    if sys.version_info.major == 3:
        from http.client import HTTPResponse
    else:
        from httplib import HTTPResponse

    source = fake_socket(response_error(500, 'Internal Server Error'))
    response = HTTPResponse(source)
    response.begin()
    assert response.status == 500
    assert time.strptime(response.getheader('Date'),
                         '%a, %d %b %Y %H:%M:%S %Z')


def test_error_response_501_well_formatted(fake_socket):
    """Test that error reponse of 501 HTTP response is correct."""
    from server import response_error
    from datetime import datetime as time

    if sys.version_info.major == 3:
        from http.client import HTTPResponse
    else:
        from httplib import HTTPResponse

    source = fake_socket(response_error(501, 'Not Implemented'))
    response = HTTPResponse(source)
    response.begin()
    assert response.status == 501
    assert time.strptime(response.getheader('Date'),
                         '%a, %d %b %Y %H:%M:%S %Z')


def test_error_response_400_well_formatted(fake_socket):
    """Test that error reponse of 400 HTTP response is correct."""
    from server import response_error
    from datetime import datetime as time

    if sys.version_info.major == 3:
        from http.client import HTTPResponse
    else:
        from httplib import HTTPResponse

    source = fake_socket(response_error(400, 'Bad Request'))
    response = HTTPResponse(source)
    response.begin()
    assert response.status == 400
    assert time.strptime(response.getheader('Date'),
                         '%a, %d %b %Y %H:%M:%S %Z')


def test_error_response_404_well_formatted(fake_socket):
    """Test that error reponse of 404 HTTP response is correct."""
    from server import response_error
    from datetime import datetime as time

    if sys.version_info.major == 3:
        from http.client import HTTPResponse
    else:
        from httplib import HTTPResponse

    source = fake_socket(response_error(404, 'Not Found'))
    response = HTTPResponse(source)
    response.begin()
    assert response.status == 404
    assert time.strptime(response.getheader('Date'),
                         '%a, %d %b %Y %H:%M:%S %Z')


def test_error_response_405_well_formatted(fake_socket):
    """Test that error reponse of 405 HTTP response is correct."""
    from server import response_error
    from datetime import datetime as time

    if sys.version_info.major == 3:
        from http.client import HTTPResponse
    else:
        from httplib import HTTPResponse

    source = fake_socket(response_error(405, 'Method Not Allowed'))
    response = HTTPResponse(source)
    response.begin()
    assert response.status == 405
    assert time.strptime(response.getheader('Date'),
                         '%a, %d %b %Y %H:%M:%S %Z')


def test_valid_parse_http_request():
    """Test the parse_request accepts valid GET http request."""
    from server import parse_request
    req = b'GET /index.html HTTP/1.1\r\n\
Host: www.example.com\r\n\
\r\n'
    assert parse_request(req) == b'/index.html'


def test_request_parse_invalid_missing_host_header():
    """Test for invalid missing host header."""
    from server import parse_request
    req = b'GET /index.html HTTP/1.1\r\n\
From: frog@j.money.com\r\n\
User-Agent: Mozilla/3.0Gold\r\n\
\r\n'
    with pytest.raises(ValueError):
        parse_request(req)


def test_request_parse_invalid_number_of_lines():
    """Test if not three lines in request, raises ValueError."""
    from server import parse_request
    req = b'GET /index.html HTTP/1.1\r\n\
Host: www.example.com\r\n'
    with pytest.raises(ValueError):
        parse_request(req)


def test_request_parse_invalid_line_formatting():
    """Test if line is properly formatted with carriage returns."""
    from server import parse_request
    req = b'GET /index.html HTTP/1.1\r\n\
Host: www.example.com\r\n\
DATE:\r\n'
    with pytest.raises(ValueError):
        parse_request(req)


def test_request_parse_invalid_method_uri_protocol_line_formatting():
    """Test if the first line of req is properly formatted with white space."""
    from server import parse_request
    req = b'GET / index.html HTTP/1.1\r\n\
Host: www.example.com\r\n\
\r\n'
    with pytest.raises(ValueError):
        parse_request(req)


@pytest.mark.parametrize('method', ['POST', 'PUT', 'DELETE', 'HEAD', 'get'])
def test_request_parse_invalid_method_is_not_get(method):
    """Test if the method is for a GET request."""
    from server import parse_request
    req = '{} /index.html HTTP/1.1\r\n\
Host: www.example.com\r\n\
\r\n'.format(method).encode('utf8')
    with pytest.raises(NotImplementedError):
        parse_request(req)


@pytest.mark.parametrize('protocol', ['HTTP/1.2', 'HTTP/1.0', 'HTTP',
                                      'http/1.1'])
def test_request_parse_invalid_protocol_is_not_http_11(protocol):
    """Test if the protocol is for HTTP/1.1."""
    from server import parse_request
    req = 'GET /index.html {}\r\n\
Host: www.example.com\r\n\
\r\n'.format(protocol).encode('utf8')
    with pytest.raises(NotImplementedError):
        parse_request(req)


def test_request_parse_invalid_uri_is_not_file_path():
    """Test if the uri is a valid file path."""
    from server import parse_request
    req = b'GET index.html HTTP/1.1\r\n\
Host: www.example.com\r\n\
\r\n'
    with pytest.raises(ValueError):
        parse_request(req)


def test_request_parse_invalid_left_justified_header_name():
    """Test if the header name is left justifiied."""
    from server import parse_request
    req = b'GET /index.html HTTP/1.1\r\n\
Host: www.example.com\r\n\
    Content-Type: text/plain\r\n\
\r\n'
    with pytest.raises(ValueError):
        parse_request(req)


def test_request_parse_invalid_missing_colon_header_name():
    """Test if the header name is missing a colon."""
    from server import parse_request
    req = b'GET /index.html HTTP/1.1\r\n\
Host: www.example.com\r\n\
Content-Type : text/plain\r\n\
\r\n'
    with pytest.raises(ValueError):
        parse_request(req)


def test_request_parse_invalid_url_for_host_value():
    """Test if the URL for the Host uses proper characters."""
    from server import parse_request
    req = b'GET /index.html HTTP/1.1\r\n\
Host: www.example.com!\r\n\
Content-Type: text/plain\r\n\
\r\n'
    with pytest.raises(ValueError):
        parse_request(req)


def test_request_parse_invalid_url_with_unicode_for_host_value():
    """Test if the URL for the Host does not use accented characters."""
    from server import parse_request
    req = b'GET /index.html HTTP/1.1\r\n\
Host: www.ex\xc3\xa5mple.com!\r\n\
Content-Type: text/plain\r\n\
\r\n'
    with pytest.raises(ValueError):
        parse_request(req)

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
