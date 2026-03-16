# SYM-L2 | p=2 | Cryptographic Fingerprint
# Content is identified by what it IS.
# Same content = same hash, anywhere, forever.

import hashlib
import numpy as np


def source_fingerprint(audio: np.ndarray) -> str:
    """SHA-256 fingerprint of audio data (first 16 hex chars)."""
    return hashlib.sha256(audio.tobytes()).hexdigest()[:16]


def frame_tag(frame_idx: int, freq: float, rms: float) -> str:
    """Deterministic 8-char hex tag from frame identity."""
    src = f"{frame_idx}:{freq:.2f}:{rms:.6f}"
    return hashlib.md5(src.encode()).hexdigest()[:8].upper()
