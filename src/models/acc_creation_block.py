from typing import Optional
from datetime import datetime
from operation import Operation
from block import Block


class AccCreationBlock(Block):
    def __init__(self, owner_name: str, amount: float, date: datetime, hash_s: str):
        super().__init__(owner_name, Operation.DEPOSIT, amount, hash_s)

        self.date = date
