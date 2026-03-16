# SYM-L5 | p=5 | AudioProcessor Core
# Harmonic extraction engine. Content sovereignty.

import numpy as np
from dataclasses import asdict
from konomi.p2_identity.constants import SYMB_VERSION, KONOMI_CONSTANT
from konomi.p2_identity.types import HarmonicFrame, SYMBSignature
from konomi.p2_identity.fingerprint import source_fingerprint
from .extraction import extract_frames
from .sacred_verb import assign_sacred_verb


class AudioProcessor:
    """SpiralSense harmonic extraction engine."""

    def __init__(self, sample_rate=22050, frame_size=2048,
                 hop_size=512, n_harmonics=8, verbose=True):
        self.sample_rate = sample_rate
        self.frame_size = frame_size
        self.hop_size = hop_size
        self.n_harmonics = n_harmonics
        self.verbose = verbose

    def process_array(self, audio, sr=None, source_label="array"):
        """Process raw audio array -> SYMBSignature."""
        sr = sr or self.sample_rate
        sid = source_fingerprint(audio)
        frames = extract_frames(
            audio, sr, self.frame_size,
            self.hop_size, self.n_harmonics
        )
        profile = [f.spiral_coeff for f in frames]
        dom = self._dominant_freq(frames)
        mc = float(np.mean([f.spectral_centroid for f in frames]))
        mr = float(np.mean([f.rms_energy for f in frames]))
        verb = assign_sacred_verb(mr, dom, mc)

        return SYMBSignature(
            symb_version=SYMB_VERSION, source_id=sid,
            sample_rate=sr, duration_sec=round(len(audio)/sr, 4),
            frame_count=len(frames), konomi_constant=KONOMI_CONSTANT,
            dominant_freq_hz=dom, mean_centroid_hz=round(mc, 2),
            mean_rms=round(mr, 6),
            resonance_profile=[round(v, 5) for v in profile],
            frames=[asdict(f) for f in frames],
            sacred_verb=verb,
            notes="SpiralSense | SYMBEYOND AI LLC",
        )

    @staticmethod
    def _dominant_freq(frames):
        if not frames:
            return 0.0
        peak = int(np.argmax([f.rms_energy for f in frames]))
        return frames[peak].fundamental_hz
