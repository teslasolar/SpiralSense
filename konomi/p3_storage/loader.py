# SYM-L3 | p=3 | Audio Loader
# Local-first data access. No cloud required.

import numpy as np
import os

try:
    import librosa
    _LIBROSA = True
except ImportError:
    _LIBROSA = False

try:
    import soundfile as sf
    _SF = True
except ImportError:
    _SF = False


def load_audio(filepath: str, sr: int = 44100):
    """Load audio file -> (waveform, sample_rate)."""
    if filepath and os.path.exists(filepath):
        try:
            if _SF:
                y, file_sr = sf.read(filepath)
                if y.ndim > 1:
                    y = np.mean(y, axis=1)
                if file_sr != sr and _LIBROSA:
                    y = librosa.resample(y, orig_sr=file_sr, target_sr=sr)
                    return y.astype(np.float32), sr
                return y.astype(np.float32), file_sr
            elif _LIBROSA:
                y, sr = librosa.load(filepath, sr=sr, mono=True)
                return y, sr
        except Exception as e:
            print(f"Error loading audio: {e}")

    # Fallback: test tone
    t = np.linspace(0, 2.0, int(sr * 2.0), endpoint=False)
    return (0.5 * np.sin(2 * np.pi * 220 * t)).astype(np.float32), sr
