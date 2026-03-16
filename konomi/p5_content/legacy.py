# SYM-L5 | p=5 | Legacy Dict Converter
# Converts waveform to the original dict contract.

import numpy as np
from .processor import AudioProcessor

try:
    import librosa
    _LIBROSA = True
except ImportError:
    _LIBROSA = False


def to_legacy_dict(waveform, sr):
    """Convert waveform to legacy dict format."""
    dur = len(waveform) / sr
    if dur < 0.01:
        return {"amplitude": np.array([]), "pitch": np.array([]),
                "sample_rate": sr, "duration": 0.0, "frames": 0,
                "frame_rate": 0.0, "symb": None}

    hop = 512
    amp = np.array([
        float(np.sqrt(np.mean(waveform[i:i+1024] ** 2)))
        for i in range(0, len(waveform) - 1024, hop)
    ])

    if _LIBROSA:
        try:
            pitches = librosa.yin(waveform, fmin=50, fmax=2000,
                                  sr=sr, hop_length=hop)
            pitches = np.nan_to_num(pitches, nan=0.0)
            pitches[pitches < 50] = 0.0
            pitches[pitches > 2000] = 0.0
        except Exception:
            pitches = np.zeros(len(amp))
    else:
        pitches = np.zeros(len(amp))

    n = min(len(amp), len(pitches))
    amp, pitches = amp[:n], pitches[:n]

    ap = AudioProcessor(sample_rate=sr, frame_size=2048,
                        hop_size=hop, n_harmonics=7, verbose=False)
    symb = ap.process_array(waveform, sr=sr)
    fr = n / dur if dur > 0 else 0.0

    return {"amplitude": amp, "pitch": pitches, "sample_rate": sr,
            "duration": dur, "frames": n, "frame_rate": fr, "symb": symb}
