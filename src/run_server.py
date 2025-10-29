#!/usr/bin/python3

import argparse
from models.server import Server


def main(server_port: int):
    server = Server(server_port)

    print(f"Server IP: {server.ip}")

    server.bind_socket()

    server.socket.listen(1)

    # TODO: usar threading aqui para conseguir aceitar múltiplas conexões ao mesmo tempo
    connection, client_address = server.socket.accept()

    # Keep the connection alive, exchanging messages, until it's closed
    while True:
        message_bytes = connection.recv(server.buffer_size)

        if not message_bytes:
            break  # Connection was closed

        message = message_bytes.decode()

        print(f"received data: {message}")

    connection.close()
    server.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("server_port", type=int, help="The port to run the server")

    args = parser.parse_args()

    main(args.server_port)
