#!/usr/bin/python3

import argparse
from models.client import Client


def main(client_name: str, server_ip: str, server_port: int):
    client = Client(client_name)
    client.connect_to(server_ip, server_port)

    while True:
        print("Usage:\n\t- deposit <amount>\n\t- withdraw <amount>\n\t- q to quit\n")
        message = input("Type action and amount:\n")

        (action, amount) = client.parse_message(message)

        if action is None:
            print("Invalid action.")
            continue

        elif action == "q":
            # Stop sending messages
            break

        elif action == "deposit":
            if amount <= 0:
                print("Amount cant be < 0")
            print("Depositing")

        elif action == "withdraw":
            if amount <= 0:
                print("Amount cant be < 0")
            print("Withdraw")

        message_bytes = message.encode()
        client.socket.sendall(message_bytes)

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
