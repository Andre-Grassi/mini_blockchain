from typing import Optional
from operation import Operation


class Block:
    def __init__(
        self,
        owner_name: str,
        amount: float,
        operation: Operation,
        hash_s: str,
    ):
        if amount <= 0:
            raise ValueError("amount must be positive.")

        if owner_name is None:
            raise ValueError("owner_name can't be None")

        self.owner_name = owner_name
        self.amount = amount
        self.operation = operation
        self.hash = hash_s

    def to_dict(self) -> dict:
        return {
            "owner_name": self.owner_name,
            "amount": self.amount,
            "operation": self.operation,
            "hash": self.hash,
        }

    def __repr__(self):
        return f"Block {self.owner_name} {self.operation} {self.amount}\n"
