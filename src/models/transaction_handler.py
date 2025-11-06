from src.models.server import Server

import datetime

from models.block import Block
from models.acc_creation_block import AccCreationBlock
from models.operation import Operation
from models.hash import Hash

class Transaction:
    @staticmethod
    def validation (client_name: str, amount: float):
        if amount <= 0:
            raise ValueError("Can't deposit <= 0 minicoins.")
        if client_name is None:
            raise ValueError("Client has no name")
        
    @staticmethod
    def current_balance (server: Server, client_name: str):
        for block in server.block_chain:
            if (block.owner_name == client_name):
                if (Hash.solve_hash(Hash, server, block)):
                    raise ValueError("Blockchain corrupted!")
                elif (block.operation == 'deposit'):
                    sum += block.amount
                elif (block.operation == 'withdraw'):
                    sum -= block.amount

        return sum
        
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

        new_block.hash_b = Hash.compute_hash(new_block)

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
        
        if Transaction.current_balance(server, client_name) < amount:
            raise ValueError("Can't withdraw more money than the current balance amount")

        if not (client_name in server.client_ids):
            raise ValueError("Can't withdraw value from an inexisting account")
        else:
            new_block = Block(client_name, amount, Operation.WITHDRAW)

        new_block.hash_b = Hash.compute_hash(new_block)

        server.block_chain.append(new_block)