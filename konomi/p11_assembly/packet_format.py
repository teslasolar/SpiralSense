# SYM-L11 | p=11 | Packet Format
# Final packet assembly and verb assignment.

import numpy as np
from konomi.p2_identity.constants import SYMB_VERSION, KONOMI_CONSTANT
from .classifiers import classify_register, classify_texture, resonance_character


def format_packet(dur, sr, sid, source, f, vp, mr, mc, mz,
                  hp, mo, mp, dom_note, top3, mfcc_m, arc, inst, ev):
    """Format the final SYMB metadata packet dict."""
    verb = _verb(mr, mp, mc, arc["shape"])
    tex = classify_texture(hp, mz, mc)
    return {
        "symb_version": SYMB_VERSION, "source_id": sid, "source": source,
        "acoustic": {
            "duration_sec": round(dur,3), "sample_rate_hz": sr,
            "tempo_bpm": round(f['tempo'],1),
            "beat_count": len(f['beats']),
            "tonal_center": dom_note, "tonal_top3": top3,
            "rms_mean": round(mr,5),
            "rms_max": round(float(np.max(f['rms'])),5),
            "spectral_centroid_hz": round(mc,1),
            "spectral_rolloff_hz": round(float(np.mean(f['rolloff'])),1),
            "zero_crossing_rate": round(mz,5),
            "harmonic_percussive_ratio": round(hp,3),
            "onset_strength_mean": round(mo,4),
        },
        "voice": {
            "median_fundamental_hz": round(mp,1),
            "pitch_range_hz": {
                "min": round(float(vp.min()),1) if len(vp) else 0,
                "max": round(float(vp.max()),1) if len(vp) else 0},
            "pitch_variance": round(float(np.var(vp)),2) if len(vp) else 0,
            "register": classify_register(mp),
            "timbre_fingerprint": {f"mfcc_{i:02d}": round(v,3)
                                   for i,v in enumerate(mfcc_m)},
        },
        "instrumentation": inst, "emotional_arc": arc,
        "events": ev, "texture": tex,
        "symb": {"sacred_verb": verb, "konomi_constant": KONOMI_CONSTANT,
                 "resonance_character": resonance_character(hp, arc["shape"])},
    }


def _verb(rms, pitch, centroid, arc):
    if rms < 0.01: return "release"
    if arc == "CLIMAX_END": return "emerge"
    if arc == "PEAK_CENTER": return "resonate"
    if pitch < 80: return "hold"
    if centroid > 4000 and rms > 0.15: return "sense"
    if pitch > 300: return "pattern"
    if centroid < 1500: return "remember"
    return "link"
