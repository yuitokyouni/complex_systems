# 実験 01: ロジスティック写像 → 分岐図

**分野**: 非線形力学系 / **スタック**: Jupyter

たった 1 行の非線形写像

$$x_{n+1} = r\, x_n (1 - x_n)$$

から、不動点 → 周期倍分岐 → カオスへの遷移を可視化する。複雑系の「少数の決定論的ルールから豊かな挙動が生まれる」という核心を体感するのが狙い。理論的背景は [`../../notes/nonlinear_dynamics.md`](../../notes/nonlinear_dynamics.md) を参照。

## 中身（`logistic_map.ipynb`）

1. **時系列**: 代表的な $r$（収束 / 周期 2 / 周期 4 / カオス）での軌道
2. **コブウェブ図**: 写像の反復を幾何学的に可視化
3. **分岐図**: $r$ を掃引したときの長期的なアトラクタ
4. **Lyapunov 指数** $\lambda(r)$: カオスの定量化、分岐図との対応
5. **ファイゲンバウム定数**の数値推定

## 実行方法

```bash
pip install -r ../../requirements.txt
jupyter notebook logistic_map.ipynb
# または出力込みで再実行:
jupyter nbconvert --to notebook --execute --inplace logistic_map.ipynb
```

## 気づき（実験後に追記する欄）

- 分岐図と Lyapunov 指数 $\lambda(r)$ は完全に対応する。$\lambda$ が 0 を上にまたぐ点でカオスに突入し、$\lambda<0$ に戻る箇所が周期窓（例: $r\approx3.83$ の周期 3）。
- ファイゲンバウム定数 $\delta\approx4.669$ は写像の詳細に依らない普遍定数 → 「ミクロの詳細に依らないマクロな法則性」という複雑系の中心テーマの最初の実例。
- 次の実験（02 Kuramoto / marimo）では、同じ「分岐・臨界」を**スライダーで対話的に**探り、Jupyter との使い分けを体感する。
