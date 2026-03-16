# SYM-L11 | p=11 | Metadata Extractor
# Derives SYMB metadata from waveform patterns alone.

import hashlib
import librosa
from konomi.p3_storage.writer import save_json
from .features import extract_features
from .packet_builder import build_packet


class MetadataExtractor:
    """Derives a complete SYMB metadata packet from audio."""

    def __init__(self, sr=44100, hop=512, verbose=True):
        self.sr, self.hop, self.verbose = sr, hop, verbose

    def extract(self, filepath):
        y, sr = librosa.load(filepath, sr=self.sr, mono=True)
        return self.extract_from_array(y, sr, source=filepath)

    def extract_from_array(self, y, sr, source="array"):
        dur = len(y) / sr
        sid = hashlib.sha256(y.tobytes()).hexdigest()[:16]
        f = extract_features(y, sr, self.hop)
        return build_packet(f, dur, sid, source, self.hop, self.sr)

    def save(self, packet, filepath):
        save_json(packet, filepath)
