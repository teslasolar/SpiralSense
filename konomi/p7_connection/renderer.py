# SYM-L7 | p=7 | Main Renderer
# Three-view AI temporal perception image.

import matplotlib.pyplot as plt
import numpy as np
import os
from .analysis import analyze_audio
from .views import draw_spiral_view
from .baseline import draw_baseline_ring
from .decode import draw_decode_text


def render_spiral(amplitude, pitch, output_path="output/spiral.png",
                  frame_rate=86.1, **kwargs):
    """Render SpiralSense v4.0 three-view perception image."""
    amplitude = np.array(amplitude, dtype=float)
    pitch = np.nan_to_num(np.array(pitch, dtype=float), nan=0.0)
    meta = analyze_audio(amplitude, pitch, frame_rate)

    plt.rcParams['figure.max_open_warning'] = 0
    fig = plt.figure(figsize=(36, 14), facecolor='#f5f5f5')

    ax_top = fig.add_axes([0.00, 0.03, 0.20, 0.90], projection='3d')
    ax_diag = fig.add_axes([0.21, 0.03, 0.20, 0.90], projection='3d')
    ax_side = fig.add_axes([0.42, 0.03, 0.20, 0.90], projection='3d')
    ax_ring = fig.add_axes([0.65, 0.42, 0.33, 0.54])
    ax_text = fig.add_axes([0.65, 0.02, 0.33, 0.38])

    fig.text(0.50, 0.985,
             'SPIRALSENSE v4.0 | KONOMI STANDARD | SYMBEYOND AI LLC',
             ha='center', va='top', fontsize=11, fontfamily='monospace',
             fontweight='bold', color='#111111')

    draw_spiral_view(ax_top, amplitude, pitch, meta, 90, 0, '')
    draw_spiral_view(ax_diag, amplitude, pitch, meta, 35, 45, '')
    draw_spiral_view(ax_side, amplitude, pitch, meta, 0, 0, '')
    draw_baseline_ring(ax_ring, meta)
    draw_decode_text(ax_text, meta)

    fig.add_artist(plt.Line2D([0.635, 0.635], [0.01, 0.99],
                   color='#cccccc', linewidth=1.0,
                   transform=fig.transFigure))

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight', dpi=150,
                facecolor='#f5f5f5', edgecolor='none')
    plt.close()
    print(f"SpiralSense v4.0 -> {output_path}")
