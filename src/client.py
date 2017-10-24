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
    except UnicodeEncodeError:
        pass
    c.sendall(message)

    packet = c.recv(8)
    resp = packet
    while len(packet) == 8:
        packet = c.recv(8)
        resp += packet

    c.close()
    return resp.decode('utf8')


if __name__ == '__main__':
    print(client(sys.argv[1]))
