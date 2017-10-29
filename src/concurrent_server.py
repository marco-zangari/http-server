"""Simple concurrent server built using gevent."""

from gevent.server import StreamServer
from gevent.monkey import patch_all
from server import response_ok, response_error, parse_request, resolve_uri


def server():
    """The server."""
    pass


def send_http_response(conn, address):
    """Send a properly formatted HTTP response to the client.

    Request sent by the client should be a properly formatted
    HTTP request.
    """
    pass


if __name__ == "__main__":  # pragma: no cover
    server()
