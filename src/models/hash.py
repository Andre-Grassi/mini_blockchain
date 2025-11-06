from block import Block
import hashlib
from models.block import Block
from server import Server

class Hash:
    def __init__(self):
          pass      
     
    def compute_hash(self, server: Server, block: Block) -> bytes:
        """Calculates the hash for the block using SHA256"""
        payload = block.serialize()

        hash_obj = hashlib.sha256()

        # If it's not the genesis, use last hash
        if len(server.block_chain) > 0:
            last_hash = server.block_chain[-1].hash_b
            hash_obj.update(last_hash)

        hash_obj.update(payload)

        return hash_obj.digest()
     
    def solve_hash(self, server:Server, block: Block):
        expected_hash = self.compute_hash(server, block)
        return expected_hash == block.hash_b