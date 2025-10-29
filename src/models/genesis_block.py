from typing import Optional
from datetime import datetime
from operation import Operation
from block import Block


class GenesisBlock(Block):
    def __init__(self, owner_name: str, amount: float, date: datetime):
        super().__init__(owner_name, Operation.DEPOSIT, None)

        self.date = date
