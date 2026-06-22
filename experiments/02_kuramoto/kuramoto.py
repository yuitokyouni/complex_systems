"""Kuramoto 結合振動子モデルのシミュレーション本体（importable）。

    dθ_i/dt = ω_i + (K/N) Σ_j sin(θ_j − θ_i)
            = ω_i + K · r · sin(ψ − θ_i)      （平均場表現）

秩序変数 r·e^{iψ} = (1/N) Σ_j e^{iθ_j} は同期の度合いを表す
（r=0 でバラバラ、r=1 で完全同期）。平均場表現を使うので 1 ステップ O(N)。
"""
import numpy as np


def order_parameter(theta):
    """秩序変数 (r, ψ) を返す。"""
    z = np.mean(np.exp(1j * theta))
    return np.abs(z), np.angle(z)


def _deriv(theta, omega, K):
    r, psi = order_parameter(theta)
    return omega + K * r * np.sin(psi - theta)


def _rk4_step(theta, omega, K, dt):
    k1 = _deriv(theta, omega, K)
    k2 = _deriv(theta + 0.5 * dt * k1, omega, K)
    k3 = _deriv(theta + 0.5 * dt * k2, omega, K)
    k4 = _deriv(theta + dt * k3, omega, K)
    return theta + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)


def simulate(K, omega, theta0=None, dt=0.05, T=40.0, seed=0):
    """結合強度 K で時間発展させ、軌道と秩序変数の時系列を返す。

    返り値: dict(t, theta(最終), r_t, psi_t, theta_traj)
    """
    n = len(omega)
    rng = np.random.default_rng(seed)
    theta = (rng.uniform(0, 2 * np.pi, n) if theta0 is None else theta0.copy())
    n_steps = int(T / dt)
    t = np.arange(n_steps) * dt
    r_t = np.empty(n_steps)
    psi_t = np.empty(n_steps)
    traj = np.empty((n_steps, n))
    for i in range(n_steps):
        r_t[i], psi_t[i] = order_parameter(theta)
        traj[i] = theta
        theta = _rk4_step(theta, omega, K, dt)
    return {"t": t, "theta": theta, "r_t": r_t, "psi_t": psi_t, "theta_traj": traj}


def mean_order_parameter(K, omega, frac=0.5, **kw):
    """定常状態での秩序変数 r を、後半 frac の時間平均で推定する。"""
    out = simulate(K, omega, **kw)
    cut = int(len(out["r_t"]) * (1 - frac))
    return out["r_t"][cut:].mean()


def critical_coupling_gaussian(sigma):
    """正規分布の自然振動数 g(ω) に対する理論的な臨界結合強度 Kc = 2/(π g(0))。"""
    g0 = 1.0 / (sigma * np.sqrt(2 * np.pi))
    return 2.0 / (np.pi * g0)


def gaussian_frequencies(n, sigma=1.0, seed=1):
    """平均 0・標準偏差 sigma の自然振動数を生成する。"""
    return np.random.default_rng(seed).normal(0.0, sigma, n)
