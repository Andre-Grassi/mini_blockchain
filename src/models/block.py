from typing import Optional
from operation import Operation


class Block:
    def __init__(
        self,
        owner_name: str,
        amount: float,
        operation: Operation,
        last_hash: Optional[str] = None,
    ):
        if amount <= 0:
            raise ValueError("amount must be positive.")

        if owner_name is None:
            raise ValueError("owner_name can't be None")

        self.amount = amount
        self.operation = operation
        self.hash = self.compute_hash(last_hash)

    def compute_hash(self, last_hash: Optional[str] = None) -> str:
        if last_hash is None:
            print("Computing hash of the first block")
        else:
            print("Computing hash")

        return "hash placeholder"
