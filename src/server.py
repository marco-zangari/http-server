"""Simple server built using socket."""

import socket


def server():
    """Start a new server until user presses control D."""
    try:
        s = socket.socket(socket.AF_INET,
                          socket.SOCK_STREAM,
                          socket.IPPROTO_TCP)
        s.bind(('127.0.0.1', 3000))
        s.listen(1)
        while True:
            conn, addr = s.accept()

            packet = conn.recv(8)
            message = packet
            while len(packet) == 8:
                packet = conn.recv(8)
                message += packet

            conn.sendall(message)
            conn.close()

    except KeyboardInterrupt:
        if 'conn' in locals():
            conn.close()
            print('Connection closed')
        s.close()
        print('Server closed')
