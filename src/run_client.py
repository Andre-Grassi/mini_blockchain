#!/usr/bin/python3

import argparse
from models.client import Client
from models.operation import Operation


def main(client_name: str, server_ip: str, server_port: int):
    client = Client(client_name)
    client.connect_to(server_ip, server_port)

    is_open = True
    while is_open:
        print("Usage:\n\t- deposit <amount>\n\t- withdraw <amount>\n\t- q to quit\n")
        message = input("Type action and amount:\n")

        (action, amount) = client.parse_message(message)
        client.send_str(message)

        if action is not None and action == Operation.QUIT.value:
            print("Quitting.")
            is_open = False

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
