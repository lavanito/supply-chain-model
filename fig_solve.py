"""
Figure: how the example solves itself.

One circuit and one only. Prices go down the chain, quantities come back.
With pay unindexed there is no second round.

Every number is computed from chain_solver.py.
"""
import os
import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

import chain_solver as c

TH = [0.390, 0.217, 0.544]
SG = [0.15, 0.30, 0.45]
THH, SGH = 0.15, 0.24 / 0.85
LAM, SHOCK = 0.0, 0.20
s = c.solve(TH, SG, [np.inf] * 3, THH, SGH, LAM, SHOCK)
p = s["p"] * 100
y = s["y"] * 100
al = s["alpha"] * 100
r = s["r"] * 100
w = s["w"][0] * 100
Om = float(np.prod(TH))

INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, BASE, SURF = "#e1e0d9", "#c3c2b7", "#ffffff"
BLUE, RED, PANEL = "#2a78d6", "#e34948", "#f0efec"

mpl.rcParams.update({
    "font.family": "serif", "font.serif": ["Latin Modern Roman", "DejaVu Serif"],
    "mathtext.fontset": "cm", "font.size": 9.5,
    "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
    "text.color": INK, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "legend.frameon": False, "pdf.fonttype": 42, "svg.fonttype": "none",
})


def num(v, dp=2, sign=True):
    t = f"{v:+.{dp}f}" if sign else f"{v:.{dp}f}"
    return t.replace("-", "−")


fig = plt.figure(figsize=(7.2, 4.3))

# ------------------------------------------------------------------ top panel
ax = fig.add_axes([0.0, 0.03, 1.0, 0.80])
ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")

names = ["Seasonal\nlabour", "Harvesting", "Processing", "Retail", "Household"]
wb, gap = 15.0, 5.5
x0 = (100 - (5 * wb + 4 * gap)) / 2
yb, hb = 46, 18
cx = []
for i, nm in enumerate(names):
    x = x0 + i * (wb + gap)
    cx.append(x + wb / 2)
    face = PANEL if i in (0, 4) else SURF
    ax.add_patch(FancyBboxPatch((x, yb), wb, hb, boxstyle="round,pad=0,rounding_size=1.2",
                                facecolor=face, edgecolor=INK2 if i not in (0, 4) else MUTED,
                                linewidth=0.9))
    ax.text(x + wb / 2, yb + hb / 2, nm, ha="center", va="center", fontsize=9,
            color=INK, linespacing=1.15)

# prices forward
ax.text(x0, 93, "The price pass. Down the chain, once.", ha="left", va="bottom",
        fontsize=9.2, color=BLUE)
for i in range(4):
    a, b = cx[i], cx[i + 1]
    ax.annotate("", xy=(b - wb / 2 - 0.6, 80), xytext=(a + wb / 2 + 0.6, 80),
                arrowprops=dict(arrowstyle="-|>", color=BLUE if i < 3 else MUTED,
                                linewidth=1.6 if i < 3 else 1.1,
                                shrinkA=0, shrinkB=0, mutation_scale=14))
    if i < 3:
        ax.text((a + b) / 2, 82, f"$-(1-\\theta_{{{i+1}}})r_{{{i+1}}}$", ha="center",
                va="bottom", fontsize=8, color=BLUE)
        ax.text((a + b) / 2, 76.5, num(-(1 - TH[i]) * r[i]), ha="center", va="top",
                fontsize=8.2, color=BLUE)
for i in range(4):
    ax.text(cx[i], 68, f"{num(p[i], sign=False)}%", ha="center", va="center",
            fontsize=9.6, color=BLUE)
ax.text(cx[4], 68, "buys", ha="center", va="center", fontsize=9, color=MUTED)
ax.text(x0 - 1.5, 68, "price", ha="right", va="center", fontsize=8.5, color=BLUE)

# quantities back
ax.text(x0, 0, "The quantity pass. Back up it, once.", ha="left", va="bottom",
        fontsize=9.2, color=RED)
for i in range(3, 0, -1):
    a, b = cx[i], cx[i + 1]
    ax.annotate("", xy=(a + wb / 2 + 0.6, 20), xytext=(b - wb / 2 - 0.6, 20),
                arrowprops=dict(arrowstyle="-|>", color=RED, linewidth=1.6,
                                shrinkA=0, shrinkB=0, mutation_scale=14))
    if i < 3:
        ax.text((a + b) / 2, 22, f"$-(1-\\theta_{{{i+1}}})\\alpha_{{{i+1}}}$", ha="center",
                va="bottom", fontsize=8, color=RED)
        ax.text((a + b) / 2, 16.5, num(-(1 - TH[i]) * al[i]), ha="center", va="top",
                fontsize=8.2, color=RED)
ax.text((cx[3] + cx[4]) / 2, 22, "$-\\eta\\, p_S$", ha="center", va="bottom",
        fontsize=8, color=RED)
ax.text((cx[3] + cx[4]) / 2, 16.5, num(y[2]), ha="center", va="top", fontsize=8.2, color=RED)
for i in range(3):
    ax.text(cx[i + 1], 7, f"{num(y[i])}%", ha="center", va="center", fontsize=9.6, color=RED)
ax.text(x0 - 1.5, 7, "output", ha="right", va="center", fontsize=8.5, color=RED)

fig.text(0.0, 1.0, "How the example solves itself", ha="left", va="top",
         fontsize=11.5, color=INK)
fig.text(0.0, 0.955,
         "Prices fall along the chain by $(1-\\theta_s) r_s$ at each step, and output is then cut by "
         "$(1-\\theta_s)\\alpha_s$ at each step coming back. Nothing feeds back, so one pass each way solves it.",
         ha="left", va="top", fontsize=9, color=INK2)

fig.text(0.0, 0.0,
         "Source: the model of Section 4, calibrated in Section 5. Supply of each stage's own inputs is "
         "perfectly elastic and pay is not indexed, so no wage moves and the matrix is lower triangular.",
         ha="left", va="bottom", fontsize=7.5, color=MUTED)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(OUT, exist_ok=True)
for ext, kw in (("pdf", {}), ("png", {"dpi": 200})):
    fig.savefig(os.path.join(OUT, f"fig-solve.{ext}"), bbox_inches="tight",
                pad_inches=0.12, **kw)
plt.close(fig)
print("prices  %", np.round(p, 4))
print("output  %", np.round(y, 4))
print("wrote fig-solve")
