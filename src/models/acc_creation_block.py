from typing import Optional
from datetime import datetime
from operation import Operation
from block import Block


class AccCreationBlock(Block):
    def __init__(self, owner_name: str, amount: float, date: datetime, hash_b: bytes):
        super().__init__(owner_name, Operation.DEPOSIT, amount, hash_b)

        self.date = date
