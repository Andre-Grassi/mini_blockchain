#!/usr/bin/python3

import argparse
from models.client import Client


def main(client_name: str, server_ip: str, server_port: int):
    client = Client(client_name)
    client.connect_to(server_ip, server_port)

    while True:
        message = input("Message: ")
        client.socket.send(message)


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
