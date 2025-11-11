#
# Authors: Andre Grassi de Jesus, Ricardo Faria
#

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Tuple

from models.block import Block
from models.acc_creation_block import AccCreationBlock
from models.operation import Operation
from models.hash import Hash

# Imports Server only during static type checking (not at runtime) to avoid
# circular dependency.
if TYPE_CHECKING:
    from models.server import Server


class Transaction:
    @staticmethod
    def execute_transaction(
        server: Server, client_name: str, amount: float, operation: Operation
    ) -> Tuple[bool, str]:
        (is_valid, status) = Transaction._validate(
            server, client_name, amount, Operation.DEPOSIT
        )

        return (True, "str")

    @staticmethod
    def deposit(server: Server, client_name: str, amount: float) -> Tuple[bool, str]:
        """Processes the deposit of a client.

        Stores the deposit of the client in a new block in the blockchain.

        Args:
            client_name (str): The identification of the client, can't be empty.
            amount (float): How many minicoins are being deposited, must be
            greater than 0.

        Returns:
            Bool indicating if the validation was ok, and a status message:
            (bool, str)

        """

        (is_valid, status) = Transaction._validate(
            server, client_name, amount, Operation.DEPOSIT
        )

        if is_valid:
            # New client
            if not (
                client_name in server.client_ids
            ):  # FIX: incorrect, new client is identified by Name operation, so this block will never be executed here
                print("New client")
                server.client_ids.append(client_name)
                creation_time = datetime.datetime.now(datetime.timezone.utc)
                new_block = AccCreationBlock(client_name, amount, creation_time)
            else:
                new_block = Block(client_name, amount, Operation.DEPOSIT)

            prev_block = None
            if len(server.block_chain) > 0:
                prev_block = server.block_chain[-1]

            new_block.hash_b = Hash.compute_hash(server, new_block, prev_block)

            server.block_chain.append(new_block)

        return (is_valid, status)

    @staticmethod
    def withdraw(server: Server, client_name: str, amount: float) -> Tuple[bool, str]:
        """Processes the deposit of a client.

        Stores the deposit of the client in a new block in the blockchain.

        Args:
            client_name (str): The identification of the client, can't be empty.
            amount (float): How many minicoins are being deposited, must be
            greater than 0.

        Returns:
            Bool indicating if the validation was ok, and a status message:
            (bool, str)

        """
        if not (client_name in server.client_ids):
            raise ValueError("Can't withdraw value from an inexisting account")

        (is_valid, status) = Transaction._validate(
            server, client_name, amount, Operation.WITHDRAW
        )

        if is_valid:
            new_block = Block(client_name, amount, Operation.WITHDRAW)

            prev_block = None
            if len(server.block_chain) > 0:
                prev_block = server.block_chain[-1]
            new_block.hash_b = Hash.compute_hash(server, new_block, prev_block)

            server.block_chain.append(new_block)

        return (is_valid, status)

    @staticmethod
    def _validate(
        server: Server, client_name: str, amount: float, operation: Operation
    ) -> Tuple[bool, str]:
        """
        Can only validate transactions, which means that this method only
        validate Operation.DEPOSIT and Operation.WITHDRAW.

        Returns:
            Bool indicating if the validation was ok, and a status message:
            (bool, str)
        """
        if not (client_name in server.client_ids):
            raise ValueError("Can't execute transaction from an inexisting account")

        if operation not in [Operation.DEPOSIT, Operation.WITHDRAW]:
            raise ValueError("Not a valid operation to validate.")

        if client_name is None:
            return (False, "Client has no name")
        if amount <= 0:
            return (False, "Can't operate <= 0 minicoins")

        if (
            operation == Operation.WITHDRAW
            and Transaction._current_balance(server, client_name) < amount
        ):
            return (False, "Can't withdraw more money than the current balance amount")

        return (True, "ok")

    @staticmethod
    def _current_balance(server: Server, client_name: str):
        balance = 0
        for block in server.block_chain:
            if block.owner_name == client_name:
                # Check operation type
                if block.operation == Operation.DEPOSIT:
                    balance += block.amount
                elif block.operation == Operation.WITHDRAW:
                    balance -= block.amount

        return balance
