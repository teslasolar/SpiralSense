# SYM-L7 | p=7 | Live Mode Renderer
# Real-time single-frame spiral drawing.

import matplotlib.pyplot as plt
import numpy as np
from .color_map import map_pitch_to_color


def render_spiral_frame(ax, amplitude, pitch, t, **kwargs):
    """Single frame for real-time live mode."""
    theta = np.linspace(t * np.pi, (t + 0.1) * np.pi, 100)
    radius = 20 + float(amplitude) * 100
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    z = np.linspace(0, float(pitch) / 5000.0 * 55, len(theta))
    color = map_pitch_to_color(float(pitch))
    lw = float(np.clip(1 + float(amplitude) * 8, 1.0, 6.0))
    ax.plot3D(x, y, z, color=color, linewidth=lw, alpha=0.8)


def setup_live_renderer():
    """Initialize live mode figure and axes."""
    plt.ion()
    fig = plt.figure(figsize=(12, 9), facecolor='black')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    ax.set_axis_off()
    ax.view_init(elev=35, azim=45)
    return fig, ax
