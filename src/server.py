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
                uri = uri if isinstance(uri, str) else uri.decode('utf8')
                response = response_ok(*resolve_uri(uri))

            except ValueError:
                response = response_error(400, 'Bad Request')

            except NotImplementedError as error:
                if 'GET' in error.args[0]:
                    response = response_error(405, 'Method Not Allowed')
                else:
                    response = response_error(501, 'Not Implmented')

            except (OSError, IOError) as error:
                response = response_error(404, 'Not Found')

            conn.sendall(response)
            conn.close()

    except KeyboardInterrupt:
        if 'conn' in locals():
            conn.close()
            print('Connection closed')
        s.close()
        print('Server closed')
        sys.exit()


def response_ok(body, mime_type):
    """Build a well formed HTTP '200 OK' response."""
    return 'HTTP/1.1 200 OK\r\n\
Date: {date}\r\n\
Content-Type: {mime_type}\r\n\
Content-Length: {length}\r\n\
\r\n'.format(date=formatdate(usegmt=True),
             mime_type=mime_type,
             length=len(body)).encode('utf8') + body


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
    """Get the file indicated by the URI and extract its contents and type.

    If the URI refers to a directory, the contents of the directory
    are listed in HTML.

    Returns: 2-tuple, body of the file as a bytestring, mimetype of file.
                      Default mimetype is text/plain.

    OSError - Access denied. URI is not inside the root directory.
    IOError - No such file or directory.
    """
    script_root_path = os.path.abspath(__file__).rsplit('/', 2)[0]

    root_path = script_root_path + '/src/webroot'

    os.chdir(root_path)

    uri = '.' + uri

    try:
        os.chdir(uri)
        if not os.getcwd().startswith(root_path):
            raise OSError('Access Denied')
        body = """<!DOCTYPE html>
<html>
<body>
"""
        for item in os.listdir('.'):
            body += item + '\n'
        body += """</body>
</html>
"""
        os.chdir(script_root_path)
        return body.encode('utf8'), 'text/html'

    except OSError as error:
        if 'No such file or directory' in error.args:
            os.chdir(script_root_path)
            raise IOError('No such file or directory: ' + error.filename)

        elif 'Not a directory' in error.args:
            dir_path, file_name = uri.rsplit('/', 1)
            os.chdir(dir_path)
            if not os.getcwd().startswith(root_path):
                raise OSError('Access Denied')

            try:
                with open(file_name, 'rb') as file:
                    body = file.read()
            except IOError as error:
                os.chdir(script_root_path)
                raise error

            file_type = guess_type(file_name)[0]

            os.chdir(script_root_path)
            return body, file_type or 'text/plain'

        else:
            os.chdir(script_root_path)
            raise error

if __name__ == "__main__":  # pragma: no cover
    server()
