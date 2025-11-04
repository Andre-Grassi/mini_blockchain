from src.models.server import Server

import datetime

from models.block import Block
from models.acc_creation_block import AccCreationBlock
from models.operation import Operation

class Transaction:
    @staticmethod
    def validation (client_name: str, amount: float):
        if amount <= 0:
            raise ValueError("Can't deposit <= 0 minicoins.")
        if client_name is None:
            raise ValueError("Client has no name")
        
    def deposit(server: Server, client_name: str, amount: float):
        """Processes the deposit of a client.

        Stores the deposit of the client in a new block in the blockchain.

        Args:
            client_name (str): The identification of the client, can't be empty.
            amount (float): How many minicoins are being deposited, must be
            greater than 0.

        """
        
        Transaction.validation(client_name, amount)

        # New client
        if not (client_name in server.client_ids):
            server.client_ids.append(client_name)
            creation_time = datetime.datetime.now(datetime.timezone.utc)
            new_block = AccCreationBlock(client_name, amount, creation_time)
        else:
            new_block = Block(client_name, amount, Operation.DEPOSIT)

        new_block.hash_b = server.compute_hash(new_block)

        server.block_chain.append(new_block)

    def withdraw(server: Server, client_name: str, amount: float):
        """Processes the deposit of a client.

        Stores the deposit of the client in a new block in the blockchain.

        Args:
            client_name (str): The identification of the client, can't be empty.
            amount (float): How many minicoins are being deposited, must be
            greater than 0.

        """
        
        Transaction.validation(client_name, amount)
        
        if not (client_name in server.client_ids):
            raise ValueError("Can't withdraw value from an inexisting account")
        else:
            new_block = Block(client_name, amount, Operation.DEPOSIT)

        new_block.hash_b = server.compute_hash(new_block)

        server.block_chain.append(new_block)