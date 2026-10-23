"""Draw the figure for miplib_benchmark.qmd from BEST_RUN.csv.

Run from the repo root: venv/bin/python articles/make_figures.py
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, "..", "BEST_RUN.csv")
OUT = os.path.join(HERE, "figures")

ACCENT = "#2f6fdb"
GREY = "#8a8f98"
INK = "#1f2328"
INK_2 = "#59606b"
GRID = "#e6e8eb"

LIMIT = 3600
X_MIN = 0.5


def certified_vs_time(d):
    total = len(d)
    presolved = int(d.jaddle_stop_reason.eq("presolve_solved").sum())
    times = np.sort(
        d.loc[d.jaddle_stop_reason.eq("certificate"), "jaddle_solve_seconds"].to_numpy()
    )
    counts = presolved + np.arange(1, len(times) + 1)
    solved = presolved + len(times)
    within_minute = presolved + int((times <= 60).sum())

    fig, ax = plt.subplots(figsize=(7.6, 4.0), dpi=200)
    x = np.concatenate([[X_MIN], times, [LIMIT]])
    y = np.concatenate([[presolved], counts, [solved]])
    ax.step(x, y, where="post", color=ACCENT, linewidth=2)

    # References: the size of the set and the time limit.
    ax.axhline(total, color=GREY, linestyle=(0, (4, 4)), linewidth=1)
    ax.axvline(LIMIT, color=GREY, linestyle=(0, (4, 4)), linewidth=1)
    ax.text(X_MIN * 1.1, total + 8, f"{total} instances in the set", color=INK_2, fontsize=9)
    ax.text(LIMIT / 1.08, 12, "1 h limit", color=INK_2, fontsize=9, ha="right")

    ax.plot([60], [within_minute], "o", color=ACCENT, markersize=6)
    ax.annotate(
        f"{within_minute} within 1 min",
        (60, within_minute),
        xytext=(8, -18),
        textcoords="offset points",
        color=INK,
        fontsize=9,
    )
    ax.text(LIMIT / 1.08, solved + 8, f"{solved} certified", color=INK, fontsize=9, ha="right")
    ax.text(LIMIT / 1.08, solved - 22, "hgms62 hit the limit", color=INK_2, fontsize=9, ha="right")

    ax.set_xscale("log")
    ax.set_xlim(X_MIN, LIMIT * 1.05)
    ax.set_ylim(0, 415)
    ax.set_xticks([1, 10, 60, 600, 3600], ["1 s", "10 s", "1 min", "10 min", "1 h"])
    ax.set_yticks([0, 100, 200, 300])
    ax.minorticks_off()
    ax.set_ylabel("Instances certified", color=INK_2)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GREY)
    ax.tick_params(colors=INK_2, length=0)

    fig.tight_layout()
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, "certified_vs_time.png"))
    plt.close(fig)


if __name__ == "__main__":
    certified_vs_time(pd.read_csv(CSV))
