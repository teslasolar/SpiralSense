# SYM-L13 | p=13 | Cascade Data Types
# MersenneCascadeFrame and Packet structures.

from dataclasses import dataclass
from typing import List


@dataclass
class MersenneCascadeFrame:
    """One audio frame translated into Lucas-Lehmer parameters."""
    frame_index:      int
    time_sec:         float
    pitch_hz:         float
    amplitude:        float
    symb_verb:        str
    mersenne_exp:     int
    mersenne_prime:   int
    register_bits:    int
    s0_seed:          int
    modulus:          int
    iteration_k:      int
    cascade_value:    int
    is_coherent:      bool
    coherence_state:  str
    coherence_pct:    float
    interference_amp: float
    spiral_radius:    float


@dataclass
class MersenneCascadePacket:
    """Full audio file translated into cascade frames."""
    source_file:      str
    duration_sec:     float
    frame_count:      int
    frame_rate:       float
    dominant_exp:     int
    dominant_prime:   int
    coherence_events: List[float]
    frames:           List[dict]
