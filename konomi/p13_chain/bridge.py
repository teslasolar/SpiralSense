# SYM-L13 | p=13 | Mersenne Bridge
# Translates SpiralSense audio into Lucas-Lehmer cascades.

import numpy as np
from dataclasses import asdict
from konomi.p5_content.sacred_verb import pitch_to_verb
from .mersenne_table import pitch_to_mersenne_exp, MERSENNE_PRIMES, VERB_TO_COHERENCE
from .lucas_lehmer import compute_ll_step, derive_s0_seed, coherence_proximity, compute_spiral_radius
from .cascade import MersenneCascadeFrame, MersenneCascadePacket


class MersenneBridge:
    """Translates audio data into Lucas-Lehmer cascade parameters."""

    def __init__(self):
        self.cascade_state = {}

    def translate_frame(self, frame_idx, time_sec, pitch_hz,
                        amplitude, symb_verb, total_frames):
        exp = pitch_to_mersenne_exp(pitch_hz)
        prime = MERSENNE_PRIMES[exp]

        if exp not in self.cascade_state:
            s0 = derive_s0_seed(pitch_hz, prime)
            self.cascade_state[exp] = {'current': s0, 'k': 0, 's0': s0}

        st = self.cascade_state[exp]
        s, k = st['current'], st['k']
        for _ in range(max(1, int(amplitude * 5))):
            s = compute_ll_step(s, prime)
            k += 1
        st['current'], st['k'] = s, k

        coherent = (s == 0)
        verb = symb_verb if symb_verb in VERB_TO_COHERENCE else 'sense'
        color = 'gold' if coherent else VERB_TO_COHERENCE.get(verb, 'blue')

        return MersenneCascadeFrame(
            frame_index=frame_idx, time_sec=time_sec,
            pitch_hz=pitch_hz, amplitude=amplitude, symb_verb=verb,
            mersenne_exp=exp, mersenne_prime=prime, register_bits=exp,
            s0_seed=st['s0'], modulus=prime, iteration_k=k,
            cascade_value=s, is_coherent=coherent,
            coherence_state=color,
            coherence_pct=round(coherence_proximity(s, prime), 4),
            interference_amp=float(amplitude),
            spiral_radius=compute_spiral_radius(frame_idx, total_frames, amplitude),
        )

    def translate(self, amplitude, pitch, frame_rate,
                  source_file="unknown", symb_verbs=None):
        amplitude = np.array(amplitude, dtype=float)
        pitch = np.nan_to_num(np.array(pitch, dtype=float), nan=0.0)
        n = len(amplitude)
        self.cascade_state = {}

        frames, coherence_events, exp_counts = [], [], {}
        for i in range(n):
            t = i / frame_rate
            p, a = float(pitch[i]), float(amplitude[i])
            verb = symb_verbs[i] if symb_verbs and i < len(symb_verbs) else pitch_to_verb(p)
            f = self.translate_frame(i, t, p, a, verb, n)
            frames.append(asdict(f))
            if f.is_coherent:
                coherence_events.append(round(t, 2))
            exp = pitch_to_mersenne_exp(p)
            exp_counts[exp] = exp_counts.get(exp, 0) + 1

        dom = max(exp_counts, key=exp_counts.get)
        return MersenneCascadePacket(
            source_file=source_file, duration_sec=n/frame_rate,
            frame_count=n, frame_rate=frame_rate,
            dominant_exp=dom, dominant_prime=MERSENNE_PRIMES[dom],
            coherence_events=coherence_events[:50], frames=frames,
        )
