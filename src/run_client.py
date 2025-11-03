#!/usr/bin/python3

#
# Authors: Andre Grassi de Jesus, Ricardo Faria
#

import argparse
from models.client import Client
from models.operation import Operation


def main(client_name: str, server_ip: str, server_port: int):
    client = Client(client_name)
    client.connect_to(server_ip, server_port)
    connection = client.socket

    # Send name to server
    client.send_str(connection, "name " + client_name)

    is_open = True
    while is_open:
        # Send command
        print("Usage:\n\t- deposit <amount>\n\t- withdraw <amount>\n\t- q to quit\n")
        message = input("Type action and amount:\n")

        (action, _) = client.parse_message(message)
        client.send_str(connection, message)

        if action is not None and action == Operation.QUIT.value:
            print("Quitting.")
            is_open = False

        # Listen server response
        message_bytes = connection.recv(client.buffer_size)

        if not message_bytes:
            break  # Connection was closed

        message = message_bytes.decode()

        print(f"received data: {message}")

    client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("client_name", type=str, help="The name of the client.")

    parser.add_argument(
        "server_ip", type=str, help="The IP of the server to connect to."
    )

    parser.add_argument(
        "server_port", type=int, help="The port of the server to connect to."
    )

    args = parser.parse_args()

    main(args.client_name, args.server_ip, args.server_port)
