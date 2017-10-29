"""Simple concurrent server built using gevent."""

import socket
import sys
from gevent.server import StreamServer
from gevent.monkey import patch_all
from server import response_ok, response_error, parse_request, resolve_uri


def server():  # pragma: no cover
    """Instantiate a new server to serve forever."""
    try:
        patch_all()
        s = StreamServer(('127.0.0.1', 3000), send_http_response)
        print('Starting server on port 3000')
        s.serve_forever()

    except KeyboardInterrupt:
        s.close()
        print('Server closed')
        sys.exit()


def send_http_response(conn, address):  # pragma: no cover
    """Send a properly formatted HTTP response to the client.

    Request sent by the client should be a properly formatted
    HTTP request.
    """
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

if __name__ == "__main__":  # pragma: no cover
    server()
