"""Simple client built using socket."""

import socket
import sys


def client(message):
    """Send message to server and return server's response."""
    c = socket.socket(socket.AF_INET,
                      socket.SOCK_STREAM,
                      socket.IPPROTO_TCP)
    c.connect(('127.0.0.1', 3000))

    try:
        message = message.encode('utf8')
    except UnicodeDecodeError:
        pass
    c.sendall(message)

    packet = c.recv(8)
    resp = packet
    while b'\r\n\r\n' not in resp:
        packet = c.recv(8)
        resp += packet

    c.close()
    return resp.decode('utf8')

if __name__ == '__main__':  # pragma: no cover
    print(client(sys.argv[1]))
