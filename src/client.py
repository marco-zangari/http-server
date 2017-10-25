"""Simple client built using socket."""

import socket
import sys


def client(message):
    """Send message to server and return server's response."""
    address = ('127.0.0.1', 3000)
    c = socket.socket(*socket.getaddrinfo(*address)[1][:3])
    c.connect(address)

    try:
        message = message.encode('utf8')
    except UnicodeDecodeError:
        pass
    c.sendall(message + b'\r\n\r\n')

    packet = c.recv(8)
    resp = packet
    while b'\r\n\r\n' not in resp:
        packet = c.recv(8)
        resp += packet

    c.close()
    return resp

if __name__ == '__main__':
    print(client(sys.argv[1]))
