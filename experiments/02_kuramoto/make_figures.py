"""実験02の代表図を figures/ に書き出す（marimo の .py は GitHub 上で図が出ないため）。
    python3 make_figures.py
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import kuramoto as kr

# 日本語フォント
_jp = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"
fm.fontManager.addfont(_jp)
plt.rcParams["font.family"] = fm.FontProperties(fname=_jp).get_name()
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.dpi"] = 120

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "figures")
os.makedirs(FIG, exist_ok=True)

N = 500
SIGMA = 1.0
omega = kr.gaussian_frequencies(N, sigma=SIGMA, seed=1)
Kc = kr.critical_coupling_gaussian(SIGMA)
print(f"理論的な臨界結合 Kc ≈ {Kc:.3f}")

# ---- 図1: 秩序変数 r(t) の時系列（弱結合 vs 強結合）----
fig, ax = plt.subplots(figsize=(8, 4))
for K, c in [(0.5, "C0"), (1.6, "C2"), (3.0, "C3")]:
    out = kr.simulate(K, omega, dt=0.05, T=40, seed=0)
    ax.plot(out["t"], out["r_t"], c, lw=1.4, label=f"K = {K}")
ax.set_xlabel("時間 t"); ax.set_ylabel("秩序変数 r")
ax.set_ylim(0, 1.02)
ax.set_title("秩序変数 r(t) の時間発展（K が大きいほど同期）")
ax.legend()
fig.tight_layout(); fig.savefig(os.path.join(FIG, "order_param_timeseries.png")); plt.close(fig)

# ---- 図2: 位相スナップショット（単位円上）----
fig, axes = plt.subplots(1, 3, figsize=(12, 4.2), subplot_kw={"aspect": "equal"})
for ax, K in zip(axes, [0.5, 1.6, 3.0]):
    out = kr.simulate(K, omega, dt=0.05, T=40, seed=0)
    th = out["theta"]
    r, psi = kr.order_parameter(th)
    circ = np.linspace(0, 2 * np.pi, 200)
    ax.plot(np.cos(circ), np.sin(circ), "0.8", lw=1)
    ax.scatter(np.cos(th), np.sin(th), s=10, c=omega, cmap="coolwarm", alpha=0.8)
    ax.arrow(0, 0, r * np.cos(psi), r * np.sin(psi), color="k",
             width=0.012, head_width=0.06, length_includes_head=True, zorder=5)
    ax.set_title(f"K = {K}   (r = {r:.2f})", fontsize=10)
    ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2); ax.axis("off")
fig.suptitle("位相スナップショット（点=振動子, 色=自然振動数, 黒矢印=秩序変数）", fontsize=12)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "phase_snapshots.png")); plt.close(fig)

# ---- 図3: 相転移図 r∞ vs K（本実験の主役）----
Ks = np.linspace(0.0, 4.0, 41)
r_inf = np.array([kr.mean_order_parameter(K, omega, frac=0.5, dt=0.05, T=40, seed=0)
                  for K in Ks])
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(Ks, r_inf, "o-", color="C0", ms=4, lw=1.2)
ax.axvline(Kc, color="C3", ls="--", lw=1)
ax.text(Kc + 0.05, 0.05, f"理論 Kc ≈ {Kc:.2f}", color="C3", fontsize=9)
ax.set_xlabel("結合強度 K"); ax.set_ylabel("定常秩序変数 r∞")
ax.set_ylim(-0.02, 1.02)
ax.set_title("同期の相転移：K が臨界値 Kc を超えると r が立ち上がる")
fig.tight_layout(); fig.savefig(os.path.join(FIG, "transition.png")); plt.close(fig)

print("wrote figures to", FIG)
