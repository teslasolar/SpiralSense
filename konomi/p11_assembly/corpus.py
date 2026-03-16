# SYM-L11 | p=11 | Corpus Reader
# One file is a snapshot. Many files is a story.

import json
import os
import glob
from datetime import datetime
from konomi.p2_identity.constants import SYMB_VERSION
from konomi.p3_storage.writer import save_json
from .corpus_analysis import overview, arc, counts, standouts


class CorpusReader:
    """Reads all SYMB metadata packets and produces corpus report."""

    def __init__(self, verbose=True):
        self.verbose = verbose

    def read(self, folder):
        packets = self._load(folder)
        if not packets:
            return {}
        packets.sort(key=lambda p: p.get("source", ""))
        return {
            "symb_version": SYMB_VERSION,
            "report_type": "SPIRALSENSE_CORPUS_REPORT",
            "generated": datetime.now().isoformat(),
            "folder": folder, "packet_count": len(packets),
            "overview": overview(packets),
            "arc": arc(packets),
            "register_map": counts(packets, "voice", "register"),
            "arc_distribution": counts(packets, "emotional_arc", "shape"),
            "verb_distribution": counts(packets, "symb", "sacred_verb"),
            "tonal_centers": counts(packets, "acoustic", "tonal_center"),
            "standouts": standouts(packets),
        }

    def save(self, report, filepath):
        save_json(report, filepath)

    def _load(self, folder):
        packets = []
        for f in glob.glob(os.path.join(folder, "meta_*.json")):
            try:
                with open(f) as fh:
                    pkt = json.load(fh)
                    pkt["_filename"] = os.path.basename(f)
                    packets.append(pkt)
            except Exception:
                pass
        return packets
