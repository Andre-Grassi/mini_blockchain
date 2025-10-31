#!/usr/bin/python3

import argparse
from models.server import Server
from models.operation import Operation


def main(server_port: int):
    server = Server(server_port)

    print(f"Server IP: {server.ip}")

    server.bind_socket()

    server.socket.listen(1)

    # TODO: usar threading aqui para conseguir aceitar múltiplas conexões ao mesmo tempo
    connection, client_address = server.socket.accept()

    # Keep the connection alive, exchanging messages, until it's closed
    is_open = True
    client_name = None
    while is_open:
        message_bytes = connection.recv(server.buffer_size)

        if not message_bytes:
            break  # Connection was closed

        message = message_bytes.decode()

        print(f"received data: {message}")

        (operation, op_data) = server.parse_message(message)

        if operation is None:
            server.send_str("Unknow operation.")
        elif operation == Operation.QUIT:
            is_open = False
        elif operation == Operation.NAME:
            client_name = op_data
        elif client_name is None:
            server.send_str("First, send your name: name <your_name>")

        # Money operations
        elif op_data <= 0:
            server.send_str("Amount must be positive.")
        elif operation == Operation.DEPOSIT:
            server.client_deposit(client_name, op_data)
        elif operation == Operation.WITHDRAW:
            raise NotImplementedError("Withdraw not implemented")
        else:
            raise RuntimeError("Unknown error")

    connection.close()
    server.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("server_port", type=int, help="The port to run the server")

    args = parser.parse_args()

    main(args.server_port)
