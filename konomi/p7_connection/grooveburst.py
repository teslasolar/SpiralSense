# SYM-L7 | p=7 | Groove Burst Renderer (OMG Mode)
# Yellow baseline. Highs erupt up. Lows plunge down.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os


def render_spiral_v4_1(amplitude, pitch, output="output/spiral_grooveburst.png"):
    """Render Groove Burst Spiral v4.1 OMG Mode."""
    amplitude = np.array(amplitude)
    pitch = np.array(pitch)
    n = min(len(amplitude), len(pitch))

    theta = np.linspace(0, 24 * np.pi, n)
    r = np.linspace(1, 10, n)
    x, y = r * np.cos(theta), r * np.sin(theta)

    amp_norm = amplitude[:n] / (np.max(np.abs(amplitude[:n])) + 1e-9)
    z_spikes = amp_norm * 5.0

    cmap_up = LinearSegmentedColormap.from_list(
        "up", ["#FFFF00", "#FFA500", "#FF0000"])
    cmap_dn = LinearSegmentedColormap.from_list(
        "dn", ["#FFFF00", "#FFA500", "#8A2BE2", "#0000FF"])

    colors = []
    for z in z_spikes:
        if z >= 0:
            colors.append(cmap_up(float(np.clip(z / 5.0, 0, 1))))
        else:
            colors.append(cmap_dn(float(np.clip(-z / 5.0, 0, 1))))
    colors = np.array(colors)

    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(x, y, np.zeros(n), color="yellow", linewidth=2.0, alpha=0.9)

    step = max(1, n // 3000)
    for i in range(0, n, step):
        ax.plot([x[i], x[i]], [y[i], y[i]], [0, z_spikes[i]],
                color=colors[i], linewidth=1.0, alpha=0.95)

    ax.view_init(elev=25, azim=35)
    ax.set_axis_off()
    ax.set_facecolor("black")
    fig.patch.set_facecolor("black")

    os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
    plt.savefig(output, dpi=300, bbox_inches="tight", facecolor="black")
    plt.close(fig)
    print(f"Groove Burst (OMG Mode) -> {output}")
