# SYM-L7 | p=7 | Decode Protocol
# Full text decode overlay for AI readers.

from konomi.p2_identity.constants import FREQ_BANDS


def draw_decode_text(ax, meta):
    """Draw decode protocol text panel."""
    dur = meta['duration']
    cd = meta['color_dist']

    cd_lines = []
    for (color, freq, name, _, _) in FREQ_BANDS:
        pct = cd.get(color, 0)
        if pct > 1.0:
            bar = '\u2588' * int(pct / 5) + '\u2591' * (20 - int(pct / 5))
            cd_lines.append(f"  {freq:<12} {bar} {pct:.0f}%  {name}")

    tm_lines = []
    for i, m in enumerate(meta['temporal_markers']):
        tm_lines.append(
            f"  [{i+1:02d}] {m['time_start']:6.1f}-{m['time_end']:5.1f}s  "
            f"amp={m['avg_amp']:.3f}  pitch={m['avg_pitch']:.0f}Hz"
        )

    text = '\n'.join([
        "SPIRALSENSE v4.0 | AI TEMPORAL PERCEPTION SYSTEM",
        "SYMBEYOND AI LLC | KONOMI STANDARD v1.0", "",
        f"  {dur:.1f}s audio encoded as light and geometry.", "",
        "THREE VIEWS:",
        "  TOP-DOWN  90deg  Pure time map",
        "  DIAGONAL  35deg  Depth + height",
        "  SIDE       0deg  Amplitude profile", "",
        "ENCODING:",
        "  CENTER = start | EDGE = end",
        f"  1 rotation = {dur/max(1,(dur/60.0)*2.0):.0f}s",
        "  COLOR = pitch | THICKNESS = amplitude", "",
        "AUDIO:",
        f"  Duration: {dur:.1f}s | Frames: {meta['frames']:,}",
        f"  Amp: {meta['amplitude_min']:.3f}-{meta['amplitude_max']:.3f}",
        f"  Pitch: {meta['pitch_min']:.0f}-{meta['pitch_max']:.0f}Hz",
        f"  Silence: {meta['silence_pct']:.1f}%", "",
        "SPECTRUM:",
    ] + cd_lines + ["", "TIMELINE:"] + tm_lines + [
        "", "fold(symbeyond) = 510,510",
    ])

    ax.text(0.03, 0.98, text, transform=ax.transAxes, fontsize=5.5,
            fontfamily='monospace', color='#111111',
            verticalalignment='top', linespacing=1.4)
    ax.set_facecolor('#f5f5f5')
    ax.axis('off')
