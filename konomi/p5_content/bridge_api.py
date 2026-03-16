# SYM-L5 | p=5 | Bridge API
# Legacy-compatible entry points for spiralsense.py.

import numpy as np
from konomi.p3_storage.loader import load_audio
from .legacy import to_legacy_dict

try:
    import librosa
    _LIBROSA = True
except ImportError:
    _LIBROSA = False


def process_audio(filepath: str, sr: int = 44100) -> dict:
    """File mode entry point. Load + process -> legacy dict."""
    waveform, sr = load_audio(filepath, sr)
    return to_legacy_dict(waveform, sr)


def process_audio_from_array(data, sr: int = 44100) -> dict:
    """Array input entry point (band-splitting)."""
    if data.ndim > 1:
        data = np.mean(data, axis=1)
    return to_legacy_dict(data.astype(np.float32), sr)


def process_audio_frame(frame, sr: int = 44100) -> dict:
    """Live mode: single buffer frame -> {amplitude, pitch}."""
    if frame.ndim > 1:
        frame = np.mean(frame, axis=1)
    rms = float(np.sqrt(np.mean(frame ** 2)))
    pitch = 0.0
    if _LIBROSA and len(frame) >= 512:
        try:
            p = librosa.yin(frame, fmin=50, fmax=2000, sr=sr)
            pitch = float(np.nan_to_num(p, nan=0.0)[0])
            if not (50 <= pitch <= 2000):
                pitch = 0.0
        except Exception:
            pass
    return {"amplitude": rms, "pitch": pitch}
