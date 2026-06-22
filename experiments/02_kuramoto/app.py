import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm

    import kuramoto as kr

    # 日本語フォント
    _jp = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"
    fm.fontManager.addfont(_jp)
    plt.rcParams["font.family"] = fm.FontProperties(fname=_jp).get_name()
    plt.rcParams["axes.unicode_minus"] = False
    return kr, mo, np, plt


@app.cell
def _(mo):
    mo.md(
        r"""
        # 実験02: Kuramoto 結合振動子 — 同期の相転移

        $$\dot\theta_i = \omega_i + \frac{K}{N}\sum_j \sin(\theta_j-\theta_i)$$

        各振動子は固有の自然振動数 $\omega_i$ を持つ。結合強度 **K** を上げると、
        ある臨界値 $K_c$ を境に、バラバラだった位相が **突然そろい始める**（同期の相転移）。
        下のスライダーを動かして体感しよう。秩序変数 $r=\left|\frac1N\sum_j e^{i\theta_j}\right|$
        が同期の度合い（0=バラバラ, 1=完全同期）。
        """
    )
    return


@app.cell
def _(mo):
    K = mo.ui.slider(0.0, 4.0, value=1.0, step=0.05, label="結合強度 K")
    N = mo.ui.slider(50, 1000, value=400, step=50, label="振動子数 N")
    sigma = mo.ui.slider(0.2, 2.0, value=1.0, step=0.1, label="自然振動数のばらつき σ")
    controls = mo.vstack([K, N, sigma])
    controls
    return K, N, sigma


@app.cell
def _(N, kr, sigma):
    # ω と理論的臨界結合は N・σ にのみ依存（K では再計算しない）
    omega = kr.gaussian_frequencies(N.value, sigma=sigma.value, seed=1)
    Kc = kr.critical_coupling_gaussian(sigma.value)
    return Kc, omega


@app.cell
def _(K, kr, omega):
    # K を動かすたびにここが再実行される（リアクティブ）
    out = kr.simulate(K.value, omega, dt=0.05, T=40, seed=0)
    r_now, psi_now = kr.order_parameter(out["theta"])
    return out, psi_now, r_now


@app.cell
def _(K, mo, r_now):
    mo.md(f"### K = {K.value:.2f} のとき　秩序変数 r ≈ **{r_now:.2f}**")
    return


@app.cell
def _(K, np, omega, out, plt, psi_now, r_now):
    # 左: r(t) の時系列 / 右: 単位円上の位相スナップショット
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.4))
    a1.plot(out["t"], out["r_t"], "C0", lw=1.4)
    a1.set_xlabel("時間 t"); a1.set_ylabel("秩序変数 r"); a1.set_ylim(0, 1.02)
    a1.set_title("r(t) の時間発展")

    th = out["theta"]
    circ = np.linspace(0, 2 * np.pi, 200)
    a2.plot(np.cos(circ), np.sin(circ), "0.8", lw=1)
    a2.scatter(np.cos(th), np.sin(th), s=12, c=omega, cmap="coolwarm", alpha=0.8)
    a2.arrow(0, 0, r_now * np.cos(psi_now), r_now * np.sin(psi_now), color="k",
             width=0.012, head_width=0.06, length_includes_head=True, zorder=5)
    a2.set_aspect("equal"); a2.axis("off")
    a2.set_xlim(-1.2, 1.2); a2.set_ylim(-1.2, 1.2)
    a2.set_title("位相スナップショット（色=自然振動数）")
    fig.tight_layout()
    fig.gca()
    fig
    return


@app.cell
def _(Kc, kr, np, omega):
    # 相転移曲線は omega（=N,σ）にのみ依存。K のスライダーでは再計算されない。
    Ks = np.linspace(0.0, 4.0, 31)
    r_inf = np.array([
        kr.mean_order_parameter(Kx, omega, frac=0.5, dt=0.05, T=30, seed=0)
        for Kx in Ks
    ])
    return Ks, r_inf


@app.cell
def _(K, Kc, Ks, plt, r_inf):
    # 相転移図 + 現在の K（この描画だけは K で安く再実行される）
    fig2, ax = plt.subplots(figsize=(8, 4))
    ax.plot(Ks, r_inf, "o-", color="C0", ms=3, lw=1.1)
    ax.axvline(Kc, color="C3", ls="--", lw=1, label=f"理論 Kc ≈ {Kc:.2f}")
    ax.axvline(K.value, color="C2", lw=1.6, label=f"現在の K = {K.value:.2f}")
    ax.set_xlabel("結合強度 K"); ax.set_ylabel("定常秩序変数 r∞")
    ax.set_ylim(-0.02, 1.02); ax.legend()
    ax.set_title("同期の相転移：K が Kc を超えると r が立ち上がる")
    fig2.tight_layout()
    fig2
    return


if __name__ == "__main__":
    app.run()
