# SYM-L5 | p=5 | Frame Extraction
# FFT-based harmonic analysis per chunk.

import numpy as np
from konomi.p2_identity.constants import KONOMI_CONSTANT
from konomi.p2_identity.types import HarmonicFrame
from konomi.p2_identity.fingerprint import frame_tag


def extract_frames(audio, sr, frame_size, hop_size, n_harmonics):
    """Extract all HarmonicFrames from audio array."""
    frames = []
    idx, num = 0, 0
    while idx + frame_size <= len(audio):
        chunk = audio[idx:idx + frame_size]
        f = _analyse_chunk(chunk, sr, num, idx, n_harmonics)
        frames.append(f)
        idx += hop_size
        num += 1
    return frames


def _analyse_chunk(chunk, sr, frame_idx, sample_pos, n_harm):
    """FFT analysis of a single audio chunk."""
    windowed = chunk * np.hanning(len(chunk))
    spectrum = np.fft.rfft(windowed)
    freqs = np.fft.rfftfreq(len(chunk), d=1.0 / sr)
    mags = np.abs(spectrum)
    phases = np.angle(spectrum)

    m = mags.copy(); m[0] = 0.0
    fund_bin = int(np.argmax(m))
    fund_hz = float(freqs[fund_bin])
    max_mag = float(mags[fund_bin]) or 1.0

    h_freqs, h_amps, h_phases = [], [], []
    for k in range(1, n_harm + 1):
        nearest = int(np.argmin(np.abs(freqs - fund_hz * k)))
        h_freqs.append(round(float(freqs[nearest]), 3))
        h_amps.append(round(min(float(mags[nearest]) / max_mag, 1.0), 5))
        h_phases.append(round(float(phases[nearest]), 5))

    mag_sum = float(np.sum(mags))
    centroid = float(np.sum(freqs * mags) / mag_sum) if mag_sum > 0 else 0.0
    geo = float(np.exp(np.mean(np.log(mags + 1e-10))))
    flatness = min(geo / (float(np.mean(mags)) + 1e-10), 1.0)
    rms = float(np.sqrt(np.mean(chunk ** 2)))

    weights = np.array([KONOMI_CONSTANT ** k for k in range(1, n_harm + 1)])
    coeff = float(np.dot(h_amps, weights))

    return HarmonicFrame(
        frame_index=frame_idx, time_sec=round(sample_pos / sr, 5),
        fundamental_hz=round(fund_hz, 3), harmonics_hz=h_freqs,
        amplitudes=h_amps, phases_rad=h_phases,
        spectral_centroid=round(centroid, 3),
        spectral_flatness=round(flatness, 5),
        rms_energy=round(rms, 6), spiral_coeff=round(coeff, 6),
        symb_tag=frame_tag(frame_idx, fund_hz, rms),
    )
