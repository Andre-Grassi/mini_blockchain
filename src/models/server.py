#
# Authors: Andre Grassi de Jesus, Ricardo Faria
#

import socket
from typing import List
import threading

from models.network_node import NetworkNode
from models.operation import Operation
from models.transaction_handler import Transaction
from models.block import Block
from models.hash import Hash


class Server(NetworkNode):
    """The server of the blockchain.

    Stores all information about the blockchain and is used by clients to
    deposit or withdraw minicoins.

    Attributes:
        ip (str): IP address of the server
        port (int): Port that the server is running
        block_chain (List[Block]): List of the blocks that constitutes the
        blockchain
        client_ids (List[str]): List of names of clients that sent messages
    """

    def __init__(self, port: int):
        super().__init__()

        self.ip = self._get_own_ip()
        self.port = port
        self.block_chain: List[Block] = []
        self.client_ids: List[str] = []

    def bind_socket(self):
        self.socket.bind((self.ip, self.port))

    # Executed in an new thread
    def answer_client(
        self, connection: socket, lock: threading.Lock, shutdown_event: threading.Event
    ) -> None:
        """Handles the communication with a client.

        Args:
            connection (socket): The socket connected to the client.
            lock (threading.Lock): Lock to protect shared state.
            shutdown_event (threading.Event): Event to signal shutdown.
        """
        # Keep the connection alive, exchanging messages, until it's closed
        is_open = True
        client_name = None
        while is_open and not shutdown_event.is_set():

            # Set short timeout to check shutdown_event periodically
            connection.settimeout(1.0)

            try:
                messages_bytes = connection.recv(self.buffer_size)
            except TimeoutError:
                # Timeout to check shutdown_event
                continue
            except OSError:
                # Connection error
                break

            if not messages_bytes:
                break  # Connection was closed

            messages = messages_bytes.decode()
            for message in messages.split("\n"):
                if message.strip() == "":
                    continue  # Ignore empty messages

                print("\n", end="")

                if client_name is not None:
                    print(f"Received from {client_name}: {message}")
                else:
                    print(f"Received from unknown client: {message}")

                (operation, op_data) = self.parse_message(message)

                if operation is None:
                    print("Sending: Unknow operation.")
                    self.send_str(connection, "Unknow operation.")
                elif operation == Operation.QUIT:
                    is_open = False
                # Cannot proceed until name is registered
                elif client_name is None:
                    if operation == Operation.NAME:
                        if op_data is not None:
                            client_name = op_data
                            if op_data not in self.client_ids:
                                self.client_ids.append(client_name)
                        else:
                            print("Sending: First, send your name: name <your_name>")
                            self.send_str(
                                connection, "First, send your name: name <your_name>"
                            )
                    else:
                        print("Sending: First, send your name: name <your_name>")
                        self.send_str(
                            connection, "First, send your name: name <your_name>"
                        )

                # Money operations
                elif operation == Operation.DEPOSIT or operation == Operation.WITHDRAW:
                    with lock:
                        (is_transaction_valid, status) = (
                            Transaction.execute_transaction(
                                self, client_name, op_data, operation
                            )
                        )

                        is_blockchain_valid = False
                        if is_transaction_valid:
                            is_blockchain_valid = Hash.validate_blockchain_hash(self)

                            if not is_blockchain_valid:
                                self.block_chain.pop()  # Pop last invalid block
                                status = "Corrupted block's hash"

                        print("Sending:", status)
                        self.send_str(connection, status)
                else:
                    raise RuntimeError("Unknown error")

                print("Blockchain:")
                if len(self.block_chain) > 0:
                    for i, block in enumerate(self.block_chain):
                        print(f"\t{i}: {block}")
                else:
                    print("\tempty")

        print("Closing connection with client " + client_name)
        self.send_str(connection, "Server shutting down connection.")
        try:
            connection.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass  # Client already closed the connection

        connection.close()
