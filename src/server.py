"""Simple server built using socket."""

import socket


def server():
    """Start a new server until user presses control D."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        s.bind(('127.0.0.1', 3000))
        s.listen(1)
        conn, addr = s.accept()
    except KeyboardInterrupt:
        if 'conn' in locals():
            conn.close()
            print('Connection closed')
        s.close()
        print('Server closed')

