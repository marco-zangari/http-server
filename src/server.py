"""Simple server built using socket."""

import socket
import sys
import os
from mimetypes import guess_type
from email.utils import formatdate
from re import match


def server():  # pragma: no cover
    """Start a new server until user presses control D."""
    try:
        s = socket.socket(socket.AF_INET,
                          socket.SOCK_STREAM,
                          socket.IPPROTO_TCP)
        s.bind(('127.0.0.1', 3000))
        s.listen(1)
        print('Server started')

        while True:
            conn, addr = s.accept()
            conn.settimeout(2)

            request = b''
            try:
                packet = conn.recv(8)
                request = packet
                while b'\r\n\r\n' not in request:
                    packet = conn.recv(8)
                    request += packet
            except socket.timeout:
                pass

            print(request.decode('utf8'))

            try:
                uri = parse_request(request)
                response = response_ok()

            except ValueError:
                response = response_error(400, 'Bad Request')

            except NotImplementedError as error:
                if 'GET' in error.args[0]:
                    response = response_error(405, 'Method Not Allowed')
                else:
                    response = response_error(501, 'Not Implmented')

            conn.sendall(response)
            conn.close()

    except KeyboardInterrupt:
        if 'conn' in locals():
            conn.close()
            print('Connection closed')
        s.close()
        print('Server closed')
        sys.exit()


def response_ok():
    """Build a well formed HTTP '200 OK' response."""
    return 'HTTP/1.1 200 OK\r\n\
Date: {}\r\n\
\r\n'.format(formatdate(usegmt=True)).encode('utf8')


def response_error(code, phrase):
    """Build a well formed HTTP Error response.

    Uses the given error code and reason phrase to create the response.
    """
    return 'HTTP/1.1 {code} {phrase}\r\n\
Date: {date}\r\n\
\r\n'.format(code=code,
             phrase=phrase,
             date=formatdate(usegmt=True)).encode('utf8')


def parse_request(req):
    """Parse the incoming HTTP request.

    ValueError - invalid fomatting
    NotImplementedError - does not accept anything but GET and HTTP/1.1
    """
    if b'\r\nHost: ' not in req:
        raise ValueError('Host header missing from request')

    req_lines = req.split(b'\r\n')

    if len(req_lines) < 4:
        raise ValueError('Improper request length')

    if req_lines[-1] or req_lines[-2]:
        raise ValueError('Improper request formatting')

    method_uri_protocol = req_lines[0].split()

    if len(method_uri_protocol) != 3:
        raise ValueError('Improper request formatting')

    if method_uri_protocol[0] != b'GET':
        raise NotImplementedError('Server only accepts GET requests')

    if not method_uri_protocol[1].startswith(b'/'):
        print(method_uri_protocol[1][0])
        raise ValueError('Improper resource path formatting')

    if method_uri_protocol[2] != b'HTTP/1.1':
        raise NotImplementedError('Server only accepts HTTP/1.1 requests')

    uri = method_uri_protocol[1]

    for header in req_lines[1:-2]:
        if header[0:1].isspace():
            raise ValueError('Improper header formatting')

        name, value = header.split(None, 1)
        if name[-1:] != b':':
            raise ValueError('Improper header formatting')

        if b'Host' in name:
            if not match('^[A-Za-z0-9_.-~]+$', value.decode('utf8')):
                raise ValueError('Improper Host formatting')

    return uri


def resolve_uri(uri):
    """Parse a request and to return a tuple."""
    current_dir = os.getcwd()

    if not current_dir.endswith('/webroot'):

        if current_dir.endswith('/http-server'):
            current_dir += '/src'

        root_dir = current_dir + '/webroot'

    else:
        root_dir = current_dir

    os.chdir(root_dir)
    print(os.getcwd())

    uri = '.' + uri
    body = b''

    try:
        os.chdir(uri)

    except OSError:
        dir_path, file_name = uri.rsplit('/', 1)
        os.chdir(dir_path)
        if 'webroot' not in os.getcwd():
            raise OSError('Access Denied')
        with open(file_name, 'rb') as file:
            body = file.read()

        file_type = guess_type(file_name)[0]

        os.chdir(root_dir)
        return body, file_type or 'text/plain'

if __name__ == "__main__":  # pragma: no cover
    server()
