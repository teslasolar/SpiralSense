# SYM-L7 | p=7 | Temporal Baseline Ring
# 2D ring visualization — time as circle.

import numpy as np


def draw_baseline_ring(ax, meta):
    """Draw 2D temporal baseline ring with energy markers."""
    duration = meta['duration']
    markers = meta['temporal_markers']
    n = len(markers)

    for i, m in enumerate(markers):
        ts = (i / n) * 2 * np.pi - np.pi / 2
        te = ((i + 1) / n) * 2 * np.pi - np.pi / 2
        theta = np.linspace(ts, te, 40)
        x = np.concatenate([0.95 * np.cos(theta), 0.55 * np.cos(theta[::-1])])
        y = np.concatenate([0.95 * np.sin(theta), 0.55 * np.sin(theta[::-1])])
        ax.fill(x, y, color=m['color'], alpha=0.88, zorder=2)
        ax.plot(np.append(x, x[0]), np.append(y, y[0]),
                color='white', linewidth=0.4, alpha=0.5, zorder=3)
        tm = (ts + te) / 2
        ax.text(1.08 * np.cos(tm), 1.08 * np.sin(tm),
                f"{m['time_start']:.0f}s", fontsize=6.5,
                ha='center', va='center', fontfamily='monospace',
                color='#222222', zorder=5)

    for i, m in enumerate(markers):
        tm = ((i + 0.5) / n) * 2 * np.pi - np.pi / 2
        pr = min(0.30 + m['avg_amp'] * 1.2, 0.52)
        ax.scatter([pr * np.cos(tm)], [pr * np.sin(tm)],
                   color=m['color'], s=max(15, m['avg_amp'] * 400),
                   alpha=0.9, zorder=6, edgecolors='white', linewidths=0.5)

    ax.text(0, 0, f"{duration/60:.1f}\nmin", ha='center', va='center',
            fontsize=8, fontfamily='monospace', color='#333333',
            fontweight='bold', zorder=7)

    mt = meta['max_tension_time']
    mta = (mt / duration) * 2 * np.pi - np.pi / 2
    ax.scatter([0.97 * np.cos(mta)], [0.97 * np.sin(mta)],
               color='white', s=80, edgecolors='red', linewidths=2, zorder=10)
    ax.text(0.97 * np.cos(mta) * 1.18, 0.97 * np.sin(mta) * 1.18,
            f"T{mt:.0f}s", fontsize=6, color='red',
            fontfamily='monospace', ha='center', va='center', zorder=11)

    for st in meta['singular_times']:
        sa = (st / duration) * 2 * np.pi - np.pi / 2
        ax.scatter([0.94 * np.cos(sa)], [0.94 * np.sin(sa)],
                   color='cyan', s=25, alpha=0.95, zorder=9,
                   edgecolors='#006666', linewidths=0.8)

    ax.text(0, -1.28, f"SILENCE: {meta['silence_pct']:.1f}%",
            ha='center', va='center', fontsize=6.5,
            fontfamily='monospace', color='#555555')

    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-1.45, 1.45)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('TEMPORAL BASELINE\nEach segment = one time slice',
                 fontsize=7.5, fontfamily='monospace', pad=10, color='#222222')
