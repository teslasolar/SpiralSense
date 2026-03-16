# SYM-L11 | p=11 | Corpus Analysis Functions
# Pattern finding across SYMB packet collections.

import numpy as np
from collections import Counter


def _g(p, *keys, d=None):
    """Safely navigate nested dict keys."""
    v = p
    for k in keys:
        v = v.get(k, d) if isinstance(v, dict) else d
    return v if v is not None else d


def counts(pkts, *keys):
    return dict(Counter([_g(p, *keys, d="?") for p in pkts]))


def overview(pkts):
    tempos = [_g(p, "acoustic", "tempo_bpm", d=0) for p in pkts]
    tempos = [t for t in tempos if t > 0]
    return {
        "dominant_register": Counter([_g(p,"voice","register",d="?") for p in pkts]).most_common(1)[0][0],
        "dominant_arc": Counter([_g(p,"emotional_arc","shape",d="?") for p in pkts]).most_common(1)[0][0],
        "dominant_verb": Counter([_g(p,"symb","sacred_verb",d="?") for p in pkts]).most_common(1)[0][0],
        "dominant_tonal_center": Counter([_g(p,"acoustic","tonal_center",d="?") for p in pkts]).most_common(1)[0][0],
        "tempo_min": round(min(tempos),1) if tempos else 0,
        "tempo_max": round(max(tempos),1) if tempos else 0,
        "tempo_mean": round(float(np.mean(tempos)),1) if tempos else 0,
    }


def arc(pkts):
    n = len(pkts)
    third = max(1, n // 3)
    regs = [_g(p,"voice","register",d="?") for p in pkts]
    r_s = Counter(regs[:third]).most_common(1)[0][0]
    r_e = Counter(regs[n-third:]).most_common(1)[0][0]
    return {
        "register_journey": f"{r_s} -> {r_e}" if r_s != r_e else f"consistent {r_s}",
    }


def standouts(pkts):
    def fn(p): return p.get("_filename","").replace("meta_","").replace(".json","")
    e = [(_g(p,"acoustic","rms_mean",d=0),p) for p in pkts]
    e.sort(key=lambda x: x[0])
    return {
        "highest_energy": {"file": fn(e[-1][1]), "rms": round(e[-1][0],5)},
        "lowest_energy": {"file": fn(e[0][1]), "rms": round(e[0][0],5)},
    }
