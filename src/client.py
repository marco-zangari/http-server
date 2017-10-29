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
    resp_head = packet
    while b'\r\n\r\n' not in resp_head:
        packet = c.recv(8)
        resp_head += packet

    headers = {line.split(b':', 1)[0]: line.split(b':', 1)[1]
               for line in resp_head.split(b'\r\n')[1:-2]}

    resp_body = b''

    body_length = int(headers.get(b'Content-Length', 0))
    acquired_body_length = len(resp_head.split(b'\r\n\r\n')[1])

    while len(resp_body) < body_length - acquired_body_length:
        packet = c.recv(8)
        resp_body += packet

    c.close()
    resp = resp_head + resp_body
    return resp.decode('utf8')

if __name__ == '__main__':  # pragma: no cover
    print(client(sys.argv[1]))
