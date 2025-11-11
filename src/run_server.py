#!/usr/bin/python3

#
# Authors: Andre Grassi de Jesus, Ricardo Faria
#

import argparse
import threading
import signal
from socket import socket

from models.server import Server
from models.operation import Operation


def main(server_port: int):

    server = Server(server_port)

    print(f"Server IP: {server.ip}")

    server.bind_socket()

    print("listening")
    server.socket.listen(1)
    print("accepting")

    # Close server on stop signals
    def close_server(signum, frame):
        print("Closing server...")
        server.close()

    signal.signal(signal.SIGINT, close_server)
    signal.signal(signal.SIGTERM, close_server)

    # Used to lock threads in synchronous functions
    lock = threading.Lock()

    # Accepting connections
    try:
        while True:
            connection, client_address = server.socket.accept()
            thread = threading.Thread(
                target=server.answer_client, args=(connection, lock)
            )
            thread.start()
            print("accepted connection")
    finally:
        server.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("server_port", type=int, help="The port to run the server")

    args = parser.parse_args()

    main(args.server_port)
