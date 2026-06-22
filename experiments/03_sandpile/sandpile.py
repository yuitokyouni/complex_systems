"""Bak–Tang–Wiesenfeld (BTW) 砂山モデル — 自己組織化臨界 (SOC) の正準モデル。

ルール:
  - 各格子点に高さ z をもつ。1 粒ずつランダムな点に砂を落とす。
  - z >= 4 の点は「崩れ」(topple)、z -= 4 し、上下左右の隣に 1 粒ずつ渡す。
  - 境界から出た粒は系外へ失われる(開放境界=散逸)。
  - 崩れが連鎖して止まるまでが一回の「雪崩」(avalanche)。

外部からの微小な駆動(1 粒)と内部の緩和(雪崩)だけで、系はパラメータ調整なしに
臨界状態へ自己組織化し、雪崩サイズがべき分布になる。崩れは numpy で並列更新する。
"""
import numpy as np

CRIT = 4  # 崩れる閾値


def new_grid(L):
    return np.zeros((L, L), dtype=np.int64)


def _distribute(z, over):
    """崩れた点 over の砂を上下左右へ 1 粒ずつ配る(境界外へは散逸)。"""
    z[over] -= CRIT
    z[1:, :] += over[:-1, :]   # 上の点から
    z[:-1, :] += over[1:, :]   # 下の点から
    z[:, 1:] += over[:, :-1]   # 左の点から
    z[:, :-1] += over[:, 1:]   # 右の点から


def relax(z):
    """安定するまで崩しきり、(size, duration, area) を返す。z は破壊的に更新。

    size     : 総崩れ回数（雪崩の大きさ）
    duration : 並列更新の段数（雪崩の継続時間）
    area     : 一度でも崩れた相異なる点の数（雪崩の広がり）
    """
    size = 0
    duration = 0
    toppled = np.zeros_like(z, dtype=bool)
    while True:
        over = z >= CRIT
        n = int(over.sum())
        if n == 0:
            break
        size += n
        duration += 1
        toppled |= over
        _distribute(z, over)
    return size, duration, int(toppled.sum())


def add_grain(z, rng, site=None):
    if site is None:
        i, j = rng.integers(0, z.shape[0]), rng.integers(0, z.shape[1])
    else:
        i, j = site
    z[i, j] += 1
    return i, j


def drive(z, n_grains, rng, warmup=0):
    """n_grains 粒を落として雪崩統計を集める。warmup 回は記録しない。

    返り値: dict(sizes, durations, areas)  (size>0 の雪崩のみ記録)
    """
    sizes, durations, areas = [], [], []
    total = warmup + n_grains
    for k in range(total):
        add_grain(z, rng)
        s, d, a = relax(z)
        if k >= warmup and s > 0:
            sizes.append(s); durations.append(d); areas.append(a)
    return {
        "sizes": np.array(sizes),
        "durations": np.array(durations),
        "areas": np.array(areas),
    }


def relax_frames(z, max_frames=400):
    """雪崩を 1 段ずつ進めながら配置のスナップショットを生成する(GIF 用)。"""
    frames = [z.copy()]
    while len(frames) < max_frames:
        over = z >= CRIT
        if not over.any():
            break
        _distribute(z, over)
        frames.append(z.copy())
    return frames


def logbin(values, n_bins=25):
    """対数等間隔ビンで分布 P(x) を推定して (中心, 確率密度) を返す。"""
    values = values[values > 0]
    lo, hi = values.min(), values.max()
    edges = np.logspace(np.log10(lo), np.log10(hi + 1), n_bins)
    counts, edges = np.histogram(values, bins=edges)
    widths = np.diff(edges)
    centers = np.sqrt(edges[:-1] * edges[1:])
    dens = counts / widths / counts.sum()
    mask = counts > 0
    return centers[mask], dens[mask]
