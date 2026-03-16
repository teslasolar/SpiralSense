# SYM-L2 | p=2 | Core Data Types
# UDTs — user-defined types FIRST.
# These are the atoms of the system.

from dataclasses import dataclass


@dataclass
class HarmonicFrame:
    """One time-slice of harmonic data."""
    frame_index:       int
    time_sec:          float
    fundamental_hz:    float
    harmonics_hz:      list
    amplitudes:        list
    phases_rad:        list
    spectral_centroid: float
    spectral_flatness: float
    rms_energy:        float
    spiral_coeff:      float
    symb_tag:          str


@dataclass
class SYMBSignature:
    """Full SYMB harmonic signature for an audio segment."""
    symb_version:      str
    source_id:         str
    sample_rate:       int
    duration_sec:      float
    frame_count:       int
    konomi_constant:   float
    dominant_freq_hz:  float
    mean_centroid_hz:  float
    mean_rms:          float
    resonance_profile: list
    frames:            list
    sacred_verb:       str
    notes:             str
