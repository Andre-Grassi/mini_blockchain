import json
from typing import Optional
from operation import Operation


class Block:
    def __init__(
        self,
        owner_name: str,
        amount: float,
        operation: Operation,
    ):
        if amount <= 0:
            raise ValueError("amount must be positive.")

        if owner_name is None:
            raise ValueError("owner_name can't be None")

        self.owner_name = owner_name
        self.amount = amount
        self.operation = operation
        self.hash_b: bytes = None

    def serialize(self) -> bytes:
        json_s = json.dumps(self.to_dict, sort_keys=True)
        return json_s.encode("utf-8")

    def to_dict(self) -> dict:
        return {
            "owner_name": self.owner_name,
            "amount": self.amount,
            "operation": self.operation,
        }

    def __repr__(self):
        if self.hash_b is not None:
            hash_hex = "None"
        else:
            hash_hex = self.hash_b.hex()
        
        return f"Block {self.owner_name} {self.operation} {self.amount}\n{hash_hex}"
