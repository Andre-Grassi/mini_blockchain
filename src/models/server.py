#
# Authors: Andre Grassi de Jesus, Ricardo Faria
#

import socket
import hashlib
from typing import List
import threading
from models.network_node import NetworkNode
from models.block import Block
from models.operation import Operation
from src.models.transaction_handler import Transaction


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

    def compute_hash(self, block: Block) -> bytes:
        """Calculates the hash for the block using SHA256"""
        payload = block.serialize()

        hash_obj = hashlib.sha256()

        # If it's not the genesis, use last hash
        if len(self.block_chain) > 0:
            last_hash = self.block_chain[-1].hash_b
            hash_obj.update(last_hash)

        hash_obj.update(payload)

        return hash_obj.digest()

    # Executed in an new thread
    def answer_client(self, connection: socket, lock: threading.Lock):
        # Keep the connection alive, exchanging messages, until it's closed
        is_open = True
        client_name = None
        while is_open:
            print(f"Blockchain: {self.block_chain}")

            message_bytes = connection.recv(self.buffer_size)

            if not message_bytes:
                break  # Connection was closed

            message = message_bytes.decode()

            print(f"received data: {message}")

            (operation, op_data) = self.parse_message(message)

            if operation is None:
                self.send_str(connection, "Unknow operation.")
            elif operation == Operation.QUIT:
                is_open = False
            elif operation == Operation.NAME:
                client_name = op_data
            elif client_name is None:
                self.send_str(connection, "First, send your name: name <your_name>")

            # Money operations
            elif op_data <= 0:
                self.send_str(connection, "Amount must be positive.")
            elif operation == Operation.DEPOSIT:
                with lock:
                    Transaction.deposit(self, client_name, op_data)
            elif operation == Operation.WITHDRAW:
                with lock:
                    Transaction.withdraw(self, client_name, op_data)
            else:
                raise RuntimeError("Unknown error")

        connection.close()

    def _get_own_ip(self) -> str:
        aux_socket = None
        try:
            # Create a UDP socket
            aux_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # Connect to an extern IP
            # 8.8.8.8 IP is a public DNS from Google
            aux_socket.connect(("8.8.8.8", 1))

            # Get local IP associated with this socket
            own_ip = aux_socket.getsockname()[0]
        except Exception as e:
            print(f"Couldn't get local IP: {e}")
        finally:
            if aux_socket:
                aux_socket.close()

        return own_ip
