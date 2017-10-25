"""Simple server built using socket."""

import socket
from email.utils import formatdate


def server():
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
            conn.settimeout(1)

            message = b''
            try:
                packet = conn.recv(8)
                message = packet
                while len(packet) == 8:
                    packet = conn.recv(8)
                    message += packet
            except socket.timeout:
                pass

            conn.sendall(message)
            conn.close()

    except KeyboardInterrupt:
        if 'conn' in locals():
            conn.close()
            print('Connection closed')
        s.close()
        print('Server closed')


def response_ok():
    """Build a well formed HTTP '200 OK' response."""
    return b'HTTP/1.1 200 OK\r\n\
Date: %b\r\n\
\r\n' % formatdate(usegmt=True).encode('utf8')


def response_error():
    """Build a well formed HTTP '500 Internal Server Error' response."""
    pass


if __name__ == "__main__":
    server()
