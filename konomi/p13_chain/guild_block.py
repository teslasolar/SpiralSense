# SYM-L13 | p=13 | Guild Block
# Immutable block structure for the guild chain.
# Each block occupies a position in 3D vector space.

import hashlib
import json
import time
from dataclasses import dataclass, field, asdict


@dataclass
class GuildBlock:
    """One block in the guild chain."""
    index:        int
    timestamp:    float
    layer:        int           # prime layer (2,3,5,7,11,13,17)
    category:     str           # 'standard','type','rule','data'
    label:        str           # human name
    payload:      dict          # encoded content
    prev_hash:    str           # hash of previous block
    nonce:        int = 0
    vector:       list = field(default_factory=lambda: [0.0, 0.0, 0.0])
    block_hash:   str = ""

    def compute_hash(self):
        raw = json.dumps({
            'index': self.index, 'timestamp': self.timestamp,
            'layer': self.layer, 'category': self.category,
            'label': self.label, 'payload': self.payload,
            'prev_hash': self.prev_hash, 'nonce': self.nonce,
        }, sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()

    def seal(self):
        self.block_hash = self.compute_hash()
        return self

    def verify(self):
        return self.block_hash == self.compute_hash()

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        return cls(**d)
