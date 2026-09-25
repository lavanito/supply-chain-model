"""
Figure: how the example solves itself.

Top panel  - one circuit. Prices go down the chain, quantities come back.
Bottom     - the circuit repeated, each round 13.2 percent of the one before.

Every number is computed from chain_solver.py.
"""
import os
import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

import chain_solver as c

TH = [0.40, 0.60, 0.50]
SG = [0.15, 0.30, 0.45]
THH, SGH = 0.15, 0.5 / 0.85
LAM, SHOCK = 0.15, 0.20
s = c.solve(TH, SG, [np.inf] * 3, THH, SGH, LAM, SHOCK)
p = s["p"] * 100
y = s["y"] * 100
al = s["alpha"] * 100
r = s["r"] * 100
w = s["w"][0] * 100
Om = float(np.prod(TH))
leak = LAM * (1 - Om)

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


fig = plt.figure(figsize=(7.2, 6.1))

# ------------------------------------------------------------------ top panel
ax = fig.add_axes([0.0, 0.365, 1.0, 0.565])
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
ax.text(x0, 93, "The price pass. Down the chain, and it repeats.", ha="left", va="bottom",
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
ax.text(x0, 0, "The quantity pass. Back up it, once, at the end.", ha="left", va="bottom",
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

# the cost of living loop
ax.annotate("", xy=(cx[1], 44.5), xytext=(cx[3], 44.5),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, linewidth=1.2, linestyle=(0, (4, 2.5)),
                            shrinkA=0, shrinkB=0, mutation_scale=12,
                            connectionstyle="arc3,rad=-0.22"))
ax.text((cx[1] + cx[3]) / 2, 33.5, f"the shelf price lifts the cost of living by "
        f"$\\lambda p_S$ = {num(w, sign=False)}%, which lifts every wage",
        ha="center", va="center", fontsize=8, color=MUTED)

fig.text(0.0, 1.0, "How the example solves itself", ha="left", va="top",
         fontsize=11.5, color=INK)
fig.text(0.0, 0.955,
         "Prices fall along the chain by $(1-\\theta_s) r_s$ at each step. Only the price pass "
         "feeds back on itself; output is then cut by $(1-\\theta_s)\\alpha_s$ at each step coming back.",
         ha="left", va="top", fontsize=9, color=INK2)

# --------------------------------------------------------------- bottom panel
ax2 = fig.add_axes([0.085, 0.085, 0.52, 0.215])
rounds = [Om * SHOCK * 100 * leak ** k for k in range(5)]
cum = np.cumsum(rounds)
xs = np.arange(1, 6)
ax2.grid(axis="y", color=GRID, linewidth=0.7)
ax2.plot(xs, cum, color=BLUE, linewidth=1.6)
ax2.plot(xs, cum, "o", color=BLUE, markersize=7, markerfacecolor=BLUE,
         markeredgecolor=SURF, markeredgewidth=1.8, zorder=4)
ax2.axhline(p[3], color=BASE, linewidth=1.0, linestyle=(0, (4, 2.5)))
ax2.text(5.45, p[3] - 0.045, f"settles at {num(p[3], sign=False)}%", ha="left", va="top",
         fontsize=8.5, color=INK2)
for i, (xx, v) in enumerate(zip(xs[:3], cum[:3])):
    ax2.annotate(f"{num(v, sign=False)}", (xx, v), textcoords="offset points",
                 xytext=(0, 9), ha="center", fontsize=8.2, color=INK)
ax2.set_xticks(xs); ax2.set_xlim(0.7, 6.6); ax2.set_ylim(2.3, 2.9)
ax2.set_xlabel("circuit"); ax2.set_ylabel("shelf price")
ax2.set_yticks([2.4, 2.6, 2.8])
ax2.set_yticklabels(["2.4%", "2.6%", "2.8%"])
for sp in ("top", "right"):
    ax2.spines[sp].set_visible(False)
ax2.spines["left"].set_color(BASE); ax2.spines["bottom"].set_color(BASE)
ax2.set_axisbelow(True)

fig.text(0.665, 0.29,
         "The shelf price lifts wages, so the price\n"
         "pass runs again. Each pass is "
         f"{leak*100:.1f} percent\n"
         f"of the one before, so they sum to a multiplier\n"
         f"of {1/(1-leak):.3f} and the shelf price settles at "
         f"{p[3]:.2f} percent.",
         ha="left", va="top", fontsize=8.8, color=INK2, linespacing=1.5)
fig.text(0.0, 0.0,
         "Source: the model of Section 4, calibrated in Section 5. Supply of each stage's own inputs is "
         "perfectly elastic, so the wage does not depend on how many are hired and quantities do not feed back.",
         ha="left", va="bottom", fontsize=7.5, color=MUTED)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(OUT, exist_ok=True)
for ext, kw in (("pdf", {}), ("png", {"dpi": 200})):
    fig.savefig(os.path.join(OUT, f"fig-solve.{ext}"), bbox_inches="tight",
                pad_inches=0.12, **kw)
plt.close(fig)
print("prices  %", np.round(p, 4))
print("output  %", np.round(y, 4))
print("rounds  %", np.round(rounds, 4), " cumulative", np.round(cum, 4))
print("leak", round(leak, 4), " multiplier", round(1 / (1 - leak), 4))
print("wrote fig-solve")
