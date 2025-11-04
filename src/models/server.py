#
# Authors: Andre Grassi de Jesus, Ricardo Faria
#

import socket
import json
import hashlib
import datetime
from typing import Optional, List
import threading
from models.network_node import NetworkNode
from models.block import Block
from models.acc_creation_block import AccCreationBlock
from models.operation import Operation


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

    def client_deposit(self, client_name: str, amount: float):
        """Processes the deposit of a client.

        Stores the deposit of the client in a new block in the blockchain.

        Args:
            client_name (str): The identification of the client, can't be empty.
            amount (float): How many minicoins are being deposited, must be
            greater than 0.

        """
        if amount <= 0:
            raise ValueError("Can't deposit <= 0 minicoins.")
        if client_name is None:
            raise ValueError("Client has no name")

        # New client
        if not (client_name in self.client_ids):
            self.client_ids.append(client_name)
            creation_time = datetime.datetime.now(datetime.timezone.utc)
            new_block = AccCreationBlock(client_name, amount, creation_time)
        else:
            new_block = Block(client_name, amount, Operation.DEPOSIT)

        new_block.hash_b = self.compute_hash(new_block)

        self.block_chain.append(new_block)

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
                    self.client_deposit(client_name, op_data)
            elif operation == Operation.WITHDRAW:
                with lock:
                    raise NotImplementedError("Withdraw not implemented")
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
