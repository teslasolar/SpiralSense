# SYM-L11 | p=11 | Raw Feature Extraction
# Pulls raw feature streams from audio via librosa.

import numpy as np
import librosa


def extract_features(y, sr, hop):
    """Extract all raw feature streams from audio."""
    rms = librosa.feature.rms(y=y, hop_length=hop)[0]
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=hop)[0]
    zcr = librosa.feature.zero_crossing_rate(y, hop_length=hop)[0]
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, hop_length=hop)[0]
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=hop)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr, hop_length=hop)

    pitch = librosa.yin(y, fmin=50, fmax=1000, sr=sr, hop_length=hop)
    pitch = np.nan_to_num(pitch, nan=0.0)
    pitch[pitch < 50] = 0.0
    pitch[pitch > 1000] = 0.0

    y_harm, y_perc = librosa.effects.hpss(y)
    harm_rms = librosa.feature.rms(y=y_harm, hop_length=hop)[0]
    perc_rms = librosa.feature.rms(y=y_perc, hop_length=hop)[0]

    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    tempo = float(np.mean(tempo))

    return {
        'rms': rms, 'centroid': centroid, 'zcr': zcr,
        'rolloff': rolloff, 'onset_env': onset_env,
        'mfcc': mfcc, 'chroma': chroma, 'pitch': pitch,
        'harm_rms': harm_rms, 'perc_rms': perc_rms,
        'tempo': tempo, 'beats': beats,
    }
