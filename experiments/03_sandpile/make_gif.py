"""臨界状態の砂山で起きる大きな雪崩をアニメーション(GIF)にする。
    python3 make_gif.py
matplotlib の FuncAnimation + PillowWriter（追加依存なし）で figures/avalanche.gif を生成。
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.animation import FuncAnimation, PillowWriter

import sandpile as sp

_jp = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"
fm.fontManager.addfont(_jp)
plt.rcParams["font.family"] = fm.FontProperties(fname=_jp).get_name()
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "figures")
os.makedirs(FIG, exist_ok=True)

L = 80
rng = np.random.default_rng(3)
z = sp.new_grid(L)

# 臨界状態まで自己組織化
for _ in range(150000):
    sp.add_grain(z, rng)
    sp.relax(z)

# 中心に砂を足して「大きな雪崩」を捕まえる（継続時間が長いものを採用）
center = (L // 2, L // 2)
frames = None
for _ in range(4000):
    zc = z.copy()
    sp.add_grain(zc, rng, site=center)
    if (zc >= sp.CRIT).any():
        f = sp.relax_frames(zc, max_frames=300)
        if len(f) > 90:          # 見応えのある長い雪崩
            frames = f
            break
    z = zc  # 雪崩が起きなければ砂を保持して次へ
    sp.relax(z)

if frames is None:
    raise RuntimeError("十分大きな雪崩が見つからなかった。seed を変えて再試行を。")

print(f"雪崩フレーム数: {len(frames)}")

fig, ax = plt.subplots(figsize=(5.2, 5.4))
im = ax.imshow(frames[0], cmap="magma", vmin=0, vmax=4, interpolation="nearest")
title = ax.set_title("砂山の雪崩（崩れの連鎖）  段 0")
ax.axis("off")
fig.colorbar(im, ax=ax, fraction=0.046, label="高さ z")
fig.tight_layout()

def update(k):
    im.set_data(frames[k])
    title.set_text(f"砂山の雪崩（崩れの連鎖）  段 {k}")
    return im, title

anim = FuncAnimation(fig, update, frames=len(frames), interval=80, blit=False)
out = os.path.join(FIG, "avalanche.gif")
anim.save(out, writer=PillowWriter(fps=12))
plt.close(fig)
print("wrote", out)
