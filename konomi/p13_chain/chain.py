# SYM-L13 | p=13 | Guild Chain Manager
# Append-only chain with validation and 3D vector placement.

import time
import json
import os
from .guild_block import GuildBlock
from .genesis import create_genesis
from .vector_space import hash_to_vector


class GuildChain:
    """Immutable append-only guild chain."""

    def __init__(self):
        self.blocks = [create_genesis()]

    def head(self):
        return self.blocks[-1]

    def append(self, layer, category, label, payload):
        prev = self.head()
        block = GuildBlock(
            index=prev.index + 1,
            timestamp=time.time(),
            layer=layer, category=category,
            label=label, payload=payload,
            prev_hash=prev.block_hash,
        )
        block.seal()
        block.vector = hash_to_vector(block.block_hash, layer, block.index)
        self.blocks.append(block)
        return block

    def validate(self):
        for i in range(1, len(self.blocks)):
            cur, prev = self.blocks[i], self.blocks[i - 1]
            if not cur.verify():
                return False, f"Block {i}: hash mismatch"
            if cur.prev_hash != prev.block_hash:
                return False, f"Block {i}: chain break"
            if cur.index != prev.index + 1:
                return False, f"Block {i}: index gap"
        return True, "Chain valid"

    def to_json(self):
        return [b.to_dict() for b in self.blocks]

    def save(self, path):
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        with open(path, 'w') as f:
            json.dump(self.to_json(), f, indent=2)

    @classmethod
    def load(cls, path):
        chain = cls.__new__(cls)
        with open(path) as f:
            data = json.load(f)
        chain.blocks = [GuildBlock.from_dict(d) for d in data]
        ok, msg = chain.validate()
        if not ok:
            raise ValueError(f"Chain invalid: {msg}")
        return chain

    def __len__(self):
        return len(self.blocks)
