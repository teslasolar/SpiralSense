# SYM-L7 | p=7 | 3D Spiral Views
# Three perspectives. Nothing hidden.

import numpy as np
from .geometry import build_spiral_geometry
from .color_map import map_pitch_to_color


def draw_spiral_view(ax, amplitude, pitch, meta, elev, azim, title):
    """Draw one 3D view of the spiral at a specific angle."""
    x, y, z, _, _ = build_spiral_geometry(amplitude, pitch, meta)
    n = len(amplitude)
    segments = 800
    pps = max(1, n // segments)

    for i in range(segments):
        s = i * pps
        e = min((i + 1) * pps, n)
        if s >= n:
            break
        sx, sy, sz = x[s:e], y[s:e], z[s:e]
        sp, sa = pitch[s:e], amplitude[s:e]
        if len(sx) == 0:
            continue
        color = map_pitch_to_color(float(np.mean(sp)))
        lw = float(np.clip(1 + np.mean(sa) * 6, 0.8, 4.0))
        ax.plot3D(sx, sy, sz, color=color, linewidth=lw, alpha=0.85)

    ax.set_xlim(-115, 115)
    ax.set_ylim(-115, 115)
    ax.set_zlim(0, 60)
    ax.set_axis_off()
    ax.view_init(elev=elev, azim=azim)
    ax.set_facecolor('#f5f5f5')
    ax.set_title(title, fontsize=7, fontfamily='monospace',
                 color='#444444', pad=4)
