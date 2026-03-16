# SYM-L11 | p=11 | Packet Builder
# Assembles the SYMB metadata packet from features.

import numpy as np
from konomi.p2_identity.constants import SYMB_VERSION, KONOMI_CONSTANT, NOTES
from .classifiers import classify_register, classify_texture, resonance_character
from .arc import extract_arc
from .instruments import detect_instrumentation
from .events import extract_events


def build_packet(f, dur, sid, source, hop, sr):
    """Build SYMB metadata packet from extracted features."""
    ml = min(len(f['rms']), len(f['pitch']), len(f['centroid']),
             len(f['zcr']), len(f['harm_rms']), len(f['perc_rms']),
             len(f['onset_env']))
    for k in ['rms','pitch','centroid','zcr','harm_rms','perc_rms','onset_env']:
        f[k] = f[k][:ml]

    vp = f['pitch'][f['pitch'] > 0]
    mr = float(np.mean(f['rms']))
    mc = float(np.mean(f['centroid']))
    mz = float(np.mean(f['zcr']))
    hp = float(np.mean(f['harm_rms']) / (np.mean(f['perc_rms']) + 1e-8))
    mo = float(np.mean(f['onset_env']))
    mp = float(np.median(vp)) if len(vp) else 0.0

    chroma_means = np.mean(f['chroma'], axis=1)
    dom_note = NOTES[int(np.argmax(chroma_means))]
    top3 = [NOTES[i] for i in np.argsort(chroma_means)[-3:][::-1]]
    mfcc_m = np.mean(f['mfcc'], axis=1).tolist()

    a = extract_arc(f['rms'], f['pitch'], hop, dur)
    inst = detect_instrumentation(hp, mc, mz, mo, mp, vp, mfcc_m)
    ev = extract_events(f['rms'], f['pitch'], f['centroid'],
                       f['onset_env'], dur, ml, hop, sr)

    from .packet_format import format_packet
    return format_packet(dur, sr, sid, source, f, vp, mr, mc, mz,
                         hp, mo, mp, dom_note, top3, mfcc_m, a, inst, ev)
