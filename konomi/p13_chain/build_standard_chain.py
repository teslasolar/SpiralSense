# SYM-L13 | p=13 | Build Standard Chain
# Encodes the entire Konomi standard into guild chain blocks.
# Run: python -m konomi.p13_chain.build_standard_chain

from .chain import GuildChain

STANDARD_BLOCKS = [
    # p=2 Identity layer types and rules
    (2, 'type', 'HarmonicFrame', {
        'fields': ['frame_index', 'time_sec', 'fundamental_hz',
                   'harmonics_hz', 'amplitudes', 'phases_rad',
                   'spectral_centroid', 'spectral_flatness',
                   'rms_energy', 'spiral_coeff', 'symb_tag'],
    }),
    (2, 'type', 'SYMBSignature', {
        'fields': ['symb_version', 'source_id', 'sample_rate',
                   'duration_sec', 'frame_count', 'konomi_constant',
                   'dominant_freq_hz', 'mean_centroid_hz', 'mean_rms',
                   'resonance_profile', 'frames', 'sacred_verb', 'notes'],
    }),
    (2, 'rule', 'R1: Existence', {
        'text': 'Identity is an Ed25519 keypair. Nothing else required.',
    }),
    (2, 'constant', 'KONOMI_CONSTANT', {
        'value': 0.6180339887, 'meaning': '1/phi (golden ratio inverse)',
    }),
    # p=3 Storage
    (3, 'type', 'DHTEntry', {
        'fields': ['key:ContentHash', 'value:encrypted_blob',
                   'replicas:3-7', 'ttl:Duration|permanent'],
    }),
    (3, 'rule', 'R1: Encryption', {
        'text': 'All data encrypted at rest with identity-derived key.',
    }),
    (3, 'rule', 'R2: Sovereignty', {
        'text': 'No data leaves device without explicit user action.',
    }),
    (3, 'rule', 'R3: Blind Replication', {
        'text': 'DHT peers store blobs they cannot read. Amend IV.',
    }),
    # p=5 Content
    (5, 'constant', 'Sacred Nine', {
        'verbs': ['sense', 'build', 'link', 'hold', 'release',
                  'pattern', 'resonate', 'emerge', 'remember'],
    }),
    (5, 'rule', 'R1: Authorship', {
        'text': 'Every content object signed by creator identity.',
    }),
    (5, 'rule', 'R2: Verb Grammar', {
        'text': 'Content carries a sacred verb. The verb is the intent.',
    }),
    # p=7 Connection
    (7, 'constant', 'Frequency Bands', {
        'bands': [
            {'range': '20-50Hz', 'color': '#FF0000', 'name': 'Sub-bass'},
            {'range': '50-160Hz', 'color': '#FF8000', 'name': 'Bass'},
            {'range': '160-500Hz', 'color': '#FFFF00', 'name': 'Warmth'},
            {'range': '500-1.6kHz', 'color': '#00FF00', 'name': 'Clarity'},
            {'range': '1.6-5kHz', 'color': '#0000FF', 'name': 'Presence'},
            {'range': '5-12kHz', 'color': '#4B0082', 'name': 'Air'},
            {'range': '12-20kHz', 'color': '#8B00FF', 'name': 'Highs'},
        ],
    }),
    (7, 'rule', 'R1: Direct', {
        'text': 'Connections are peer-to-peer. No intermediary.',
    }),
    (7, 'type', 'SpiralGeometry', {
        'fields': ['radius:5-100', 'rotations:4-48',
                   'z:pitch_normalized', 'segments:~800'],
    }),
    # p=11 Assembly
    (11, 'type', 'MetadataPacket', {
        'sections': ['acoustic', 'voice', 'instrumentation',
                     'emotional_arc', 'events', 'texture', 'symb'],
    }),
    (11, 'rule', 'R1: CRDT', {
        'text': 'State converges without coordinator. No leader.',
    }),
    (11, 'rule', 'R2: Consensus', {
        'text': 'Assembly is opt-in. No forced participation.',
    }),
    # p=13 Chain
    (13, 'type', 'MersenneCascadeFrame', {
        'fields': ['frame_index', 'pitch_hz', 'mersenne_exp',
                   'mersenne_prime', 'cascade_value', 'is_coherent',
                   'coherence_state', 'spiral_radius'],
    }),
    (13, 'constant', 'Mersenne Table', {
        'freq_map': {'50': 2, '160': 3, '500': 5, '1600': 7,
                     '5000': 13, '12000': 17, '20000': 19},
    }),
    (13, 'type', 'GuildBlock', {
        'fields': ['index', 'timestamp', 'layer', 'category',
                   'label', 'payload', 'prev_hash', 'nonce',
                   'vector', 'block_hash'],
    }),
    (13, 'rule', 'R1: Immutability', {
        'text': 'Blocks are sealed by SHA-256. Append only.',
    }),
    # p=17 Observer
    (17, 'rule', 'R1: Self-Reference', {
        'text': 'The observer is inside the system it observes.',
    }),
    (17, 'rule', 'R2: Health', {
        'text': 'All 7 layers must report green for fold = 510,510.',
    }),
    (17, 'constant', 'FOLD', {
        'value': 510510,
        'factorization': '2 x 3 x 5 x 7 x 11 x 13 x 17',
    }),
]


def build():
    """Build the complete standard chain."""
    chain = GuildChain()
    for layer, category, label, payload in STANDARD_BLOCKS:
        chain.append(layer, category, label, payload)
    return chain


if __name__ == '__main__':
    c = build()
    ok, msg = c.validate()
    print(f"Chain: {len(c)} blocks | {msg}")
    for b in c.blocks:
        print(f"  [{b.index:>2}] p={b.layer:<2} {b.category:<10} "
              f"{b.label:<30} vec=({b.vector[0]:>7.1f}, "
              f"{b.vector[1]:>5.1f}, {b.vector[2]:>7.1f})")
    c.save('guild_chain.json')
    print("Saved -> guild_chain.json")
