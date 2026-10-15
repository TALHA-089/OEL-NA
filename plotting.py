from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from outline import left_half, right_half

COLORS = {
    "Lagrange": "#d95f02",
    "Newton": "#1b9e77",
    "Cubic Spline": "#7570b3",
}
LINE_STYLES = {
    "Lagrange": {"linewidth": 6, "alpha": 0.55, "linestyle": "-"},
    "Newton": {"linewidth": 2, "alpha": 1.0, "linestyle": "--"},
    "Cubic Spline": {"linewidth": 2.5, "alpha": 1.0, "linestyle": "-"},
}
LEFT_COLOR = "#1f4e79"
RIGHT_COLOR = "#c0392b"
POINT_COLOR = "#222222"
GUIDE_COLOR = "#888888"


def style_axes(ax, title, x_limits=(-3.5, 3.5)):
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_xlabel("Horizontal position (distance from midline)")
    ax.set_ylabel("Vertical position y (face height)")
    ax.set_xlim(*x_limits)
    ax.set_ylim(-0.5, 10.5)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.3)
    ax.axvline(0.0, color=GUIDE_COLOR, linestyle="--", linewidth=1)


def plot_known_points(y_known, x_known):
    fig, ax = plt.subplots(figsize=(6, 7))
    ax.plot(-x_known, y_known, "o", color=LEFT_COLOR, markersize=9, label="Given left-side points")
    for x, y in zip(x_known, y_known):
        ax.annotate(
            f"(x={x:.1f}, y={y:.0f})",
            (-x, y),
            textcoords="offset points",
            xytext=(-12, 0),
            ha="right",
            va="center",
            fontsize=9,
        )
    style_axes(ax, "Given Data: Left Half of the Face Outline", x_limits=(-4.8, 1.2))
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", fontsize=9)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    return fig


def plot_method_comparison(y_known, x_known, curves):
    fig, ax = plt.subplots(figsize=(6, 8.5))
    for name, (y_dense, x_dense) in curves.items():
        ax.plot(-x_dense, y_dense, color=COLORS[name], label=name, **LINE_STYLES[name])
    ax.plot(-x_known, y_known, "o", color=POINT_COLOR, markersize=8, label="Given points", zorder=5)
    style_axes(ax, "Left Half: Three Interpolation Methods", x_limits=(-3.0, 0.6))
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, fontsize=9)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    return fig


def draw_face(ax, y_known, x_known, y_dense, x_dense):
    left_x, left_y = left_half(y_dense, x_dense)
    right_x, right_y = right_half(y_dense, x_dense)
    ax.plot(left_x, left_y, color=LEFT_COLOR, linewidth=2.5, label="Left half (interpolated)")
    ax.plot(right_x, right_y, color=RIGHT_COLOR, linewidth=2.5, label="Right half (mirrored)")
    ax.plot(
        [left_x[-1], right_x[-1]],
        [left_y[-1], right_y[-1]],
        color=GUIDE_COLOR,
        linestyle=":",
        linewidth=2,
        label="Top edge (closing line)",
    )
    ax.plot(-x_known, y_known, "o", color=POINT_COLOR, markersize=7, label="Given points", zorder=5)
    ax.plot(x_known[1:], y_known[1:], "o", color=POINT_COLOR, markersize=7, markerfacecolor="white", zorder=5, label="Mirrored points")
    ax.fill(
        np.concatenate([left_x, right_x[::-1]]),
        np.concatenate([left_y, right_y[::-1]]),
        color="#f5d6b8",
        alpha=0.45,
    )


def plot_full_outline(y_known, x_known, y_dense, x_dense, method_name):
    fig, ax = plt.subplots(figsize=(7, 8.5))
    draw_face(ax, y_known, x_known, y_dense, x_dense)
    style_axes(ax, f"Complete Face Outline ({method_name})")
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, fontsize=9)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    return fig


def plot_method_gallery(y_known, x_known, curves):
    fig, axes = plt.subplots(1, len(curves), figsize=(5 * len(curves), 7.5))
    for ax, (name, (y_dense, x_dense)) in zip(axes, curves.items()):
        draw_face(ax, y_known, x_known, y_dense, x_dense)
        style_axes(ax, name)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=5, fontsize=9)
    fig.suptitle("Complete Face Outline by Interpolation Method", fontsize=14, fontweight="bold")
    fig.tight_layout(rect=(0, 0.06, 1, 0.96))
    return fig


def save_figure(fig, folder, name):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / name
    fig.savefig(path, dpi=200, bbox_inches="tight")
    return path
