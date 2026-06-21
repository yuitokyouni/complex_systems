# -*- coding: utf-8 -*-
"""講義資料 PDF を生成する。
内容を変えたいときはこのスクリプトを編集して再実行する:
    python3 _build_lecture.py
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Preformatted, PageBreak, HRFlowable,
)

JP = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"
pdfmetrics.registerFont(TTFont("JP", JP))

# ---- スタイル ----
styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=styles["Heading1"], fontName="JP",
                    fontSize=16, leading=22, spaceBefore=14, spaceAfter=8,
                    textColor=colors.HexColor("#1a3a5c"))
H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="JP",
                    fontSize=12.5, leading=18, spaceBefore=10, spaceAfter=5,
                    textColor=colors.HexColor("#2a6090"))
BODY = ParagraphStyle("BODY", parent=styles["BodyText"], fontName="JP",
                      fontSize=10, leading=16, spaceAfter=5)
BULLET = ParagraphStyle("BULLET", parent=BODY, leftIndent=12, spaceAfter=2)
CODE = ParagraphStyle("CODE", parent=styles["Code"], fontName="JP",
                      fontSize=8.5, leading=11.5, backColor=colors.HexColor("#f2f4f7"),
                      borderColor=colors.HexColor("#d0d7de"), borderWidth=0.5,
                      borderPadding=6, leftIndent=2, spaceBefore=3, spaceAfter=7)
TITLE = ParagraphStyle("TITLE", parent=BODY, fontName="JP", fontSize=22,
                       leading=30, alignment=TA_CENTER, textColor=colors.HexColor("#12243a"))
SUB = ParagraphStyle("SUB", parent=BODY, fontName="JP", fontSize=11,
                     leading=16, alignment=TA_CENTER, textColor=colors.HexColor("#55606b"))
CAP = ParagraphStyle("CAP", parent=BODY, fontSize=8.5, leading=12,
                     textColor=colors.HexColor("#55606b"))

story = []
def h1(t): story.append(Paragraph(t, H1))
def h2(t): story.append(Paragraph(t, H2))
def p(t):  story.append(Paragraph(t, BODY))
def b(t):  story.append(Paragraph("・ " + t, BULLET))
def code(t): story.append(Preformatted(t, CODE))
def sp(h=4): story.append(Spacer(1, h))
def rule(): story.append(HRFlowable(width="100%", thickness=0.6,
                                     color=colors.HexColor("#c8d0d8"), spaceBefore=4, spaceAfter=8))

def table(data, col_widths, header=True):
    t = Table(data, colWidths=col_widths, hAlign="LEFT")
    ts = [
        ("FONT", (0, 0), (-1, -1), "JP", 9),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c8d0d8")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]
    if header:
        ts += [("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a3a5c")),
               ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
               ("FONT", (0, 0), (-1, 0), "JP", 9.5)]
        ts += [("ROWBACKGROUNDS", (0, 1), (-1, -1),
                [colors.white, colors.HexColor("#f2f4f7")])]
    t.setStyle(TableStyle(ts))
    story.append(t)
    sp(8)

# ===================== 表紙 =====================
sp(120)
story.append(Paragraph("ノートブック実験環境 入門", TITLE))
sp(6)
story.append(Paragraph("Jupyter と marimo — 使い方・使い分け・道具を深く知るということ", SUB))
sp(30)
story.append(Paragraph("complex_systems プロジェクト 講義資料 #01", SUB))
story.append(Paragraph("作成: 2026-06-21", SUB))
story.append(PageBreak())

# ===================== 0. この資料のねらい =====================
h1("0. この資料のねらい")
p("複雑系の実験は「式を書く → 数値計算する → 図にする → 気づく」の反復だ。"
  "この反復を回す主戦場が<b>ノートブック</b>環境である。本資料では二大ツール "
  "Jupyter と marimo の使い方と<b>使い分け</b>を扱う。")
p("ただし真の目的はツールの操作習得そのものではない。"
  "<b>「道具を1割しか使わない人」から「マニュアルを通読した上位数%」へ移行する</b>こと、"
  "そして<b>自分の作業を観察して環境に落とし込む習慣</b>を身につけることにある。"
  "プロの作業環境の差は単一の教科書からではなく、この習慣の堆積から生まれる。")
rule()

# ===================== 1. なぜノートブックか =====================
h1("1. なぜノートブックか")
p("通常のスクリプト(.py を一括実行)と違い、ノートブックは<b>セル単位で実行</b>でき、"
  "コード・実行結果(数値や図)・文章(Markdown + 数式)を一枚の文書に混在させられる。"
  "探索的な実験 — 「このパラメータを変えると?」を即座に試して図で確かめる — に最適。")
b("<b>対話性</b>: 重い計算を一度だけ走らせ、その結果を使って何度も可視化を試せる。")
b("<b>物語性</b>: 理論メモ・コード・図・考察を順番に並べ、後から読める研究ノートになる。")
b("<b>共有性</b>: 出力込みで保存すれば、実行しなくても GitHub 上で図が見える。")
p("本プロジェクトでは <b>1 実験 = 1 ディレクトリ</b>、その中にノートブックを置く運用とする。")
rule()

# ===================== 2. Jupyter =====================
h1("2. Jupyter — 定番・計算してプロットする実験向き")
h2("2.1 起動と基本操作")
code("pip install jupyter\n"
     "jupyter notebook        # 旧来のUI\n"
     "jupyter lab             # 多機能IDE風UI（推奨）\n"
     "# 出力込みでコマンドラインから再実行（再現性チェック）:\n"
     "jupyter nbconvert --to notebook --execute --inplace 実験.ipynb")
h2("2.2 セルの種類と必須ショートカット")
p("セルは <b>Code</b>(コード) と <b>Markdown</b>(文章・数式) の2種類。"
  "コマンドモード(Escで入る・セルが青枠)と編集モード(Enterで入る)を切り替えて操作する。")
table([
    ["ショートカット", "動作"],
    ["Shift + Enter", "セルを実行して次へ"],
    ["Ctrl + Enter", "セルを実行してとどまる"],
    ["Esc → A / B", "上 / 下にセルを追加"],
    ["Esc → D D", "セルを削除"],
    ["Esc → M / Y", "Markdown / Code に変換"],
    ["Esc → Z", "操作を元に戻す"],
], [55*mm, 95*mm])
h2("2.3 数式は Markdown セルに LaTeX で書く")
code("$$x_{n+1} = r\\,x_n(1-x_n)$$       # ブロック数式\n"
     "インライン: $\\lambda > 0$ ならカオス。")
h2("2.4 Jupyter 最大のクセ: 隠れた実行状態")
p("Jupyter は<b>セルを実行した順</b>に状態(変数)が決まる。"
  "上から下に書いてあっても、実行順が違えば結果も違う。"
  "セルを消しても、その変数はカーネルのメモリに残り続ける。"
  "これが<b>「自分の手元では動くのに再現できない」</b>問題の主因。")
p("対策の作法:")
b("こまめに <b>Kernel → Restart &amp; Run All</b>(全消去して上から再実行)で再現性を確認する。")
b("コミット前に必ず nbconvert --execute で「まっさらな状態から通る」ことを確かめる。")
b("セルは<b>上から下に読めば再現できる</b>順序で並べる。")
rule()

story.append(PageBreak())

# ===================== 3. marimo =====================
h1("3. marimo — リアクティブ・対話的に挙動を探る実験向き")
h2("3.1 思想: 隠れ状態をなくす")
p("marimo は Jupyter の「隠れた実行状態」問題を設計から排除した新しいノートブック。"
  "セル間の<b>依存関係を自動で解析</b>し、あるセルの変数を変えると"
  "<b>それに依存するセルだけが自動で再実行</b>される(表計算ソフトのような<b>リアクティブ</b>性)。"
  "実行順序による不整合が原理的に起きない。")
h2("3.2 起動と保存形式")
code("pip install marimo\n"
     "marimo edit 実験.py      # 編集モードで起動\n"
     "marimo run  実験.py      # Webアプリとして起動（コードを隠して操作だけ）\n"
     "# 保存形式は .ipynb ではなく純粋な .py")
p("保存が<b>通常の .py</b>である点が効く。git の差分がコードとして綺麗に出る("
  ".ipynb は出力が JSON に混ざって差分が読みにくい)。普通の Python として import / 実行もできる。")
h2("3.3 強力な UI 要素(スライダー等)")
p("スライダーやドロップダウンを数行で置け、動かすと依存セルが即再描画される。"
  "「結合強度 K を上げると、ある点で<b>突然</b>同期する」といった相転移を体感的に探るのに最適。")
code("import marimo as mo\n"
     "K = mo.ui.slider(0.0, 4.0, value=1.0, step=0.05, label='結合強度 K')\n"
     "K                       # ← これを表示するとスライダーが出る\n"
     "\n"
     "# 別のセル: K.value を使うと、スライダーを動かす度に自動再実行\n"
     "result = simulate(coupling=K.value)\n"
     "plot(result)")
h2("3.4 marimo のクセ・制約")
b("変数名はノートブック内で<b>一意</b>でなければならない(依存解析の代償)。")
b("セルを跨いだ変数の再代入は不可。関数やスコープで囲って整理する作法が要る。")
b("エコシステムは Jupyter ほど成熟していない(資料・拡張は Jupyter が豊富)。")
rule()

# ===================== 4. 使い分け =====================
h1("4. 使い分け早見表")
table([
    ["観点", "Jupyter", "marimo"],
    ["向く実験", "計算して図を出す\n(分岐図・重い解析)", "パラメータを動かして\n挙動を探る(相転移)"],
    ["対話性", "セルを手動で再実行", "依存セルが自動で再実行\n(リアクティブ)"],
    ["再現性", "実行順に注意が必要\n(隠れ状態)", "原理的に保証\n(隠れ状態なし)"],
    ["保存形式", ".ipynb (JSON)\n出力込みで図が残る", ".py (純Python)\ngit差分が綺麗"],
    ["UI部品", "ipywidgets(やや手間)", "mo.ui.* (数行・標準)"],
    ["成熟度・資料", "非常に豊富", "発展途上"],
    ["アプリ化", "不得手", "marimo run で即Webアプリ"],
], [30*mm, 60*mm, 60*mm])
h2("本プロジェクトでの方針")
b("<b>計算結果を一度出して図にする</b>系(実験01 分岐図など) → <b>Jupyter</b>。"
  "出力込みで保存すれば GitHub でそのまま図が見える。")
b("<b>パラメータをいじって挙動を体感する</b>系(実験02 Kuramoto 同期など) → <b>marimo</b>。"
  "スライダーで臨界点を探る。")
b("迷ったら: 「動かして遊びたい」なら marimo、「結果を記録して見せたい」なら Jupyter。")
rule()

# ===================== 5. チートシート =====================
h1("5. 実践チートシート")
h2("環境構築(このリポジトリ)")
code("pip install -r requirements.txt")
h2("Jupyter")
code("jupyter lab                                     # 起動\n"
     "jupyter nbconvert --to notebook --execute \\\n"
     "        --inplace 実験.ipynb                    # 出力込みで再実行\n"
     "jupyter nbconvert --to html 実験.ipynb          # HTML書き出し")
h2("marimo")
code("marimo edit 実験.py        # 編集\n"
     "marimo run  実験.py        # アプリとして実行\n"
     "marimo convert 旧.ipynb > 新.py   # Jupyter から変換")
rule()

# ===================== 6. 次の一歩 =====================
h1("6. 次の一歩と「道具を深く知る」習慣")
p("次の実験02(Kuramoto 結合振動子)は<b>あえて marimo</b>で作る。"
  "スライダーで結合強度を上げ、バラバラだった振動子が<b>ある点で突然同期する</b>様子を"
  "対話的に観察し、実験01(Jupyter)との手触りの違いを体で覚えるのが狙いだ。")
p("最後に、本資料冒頭のねらいに戻る。プロの環境の差は買ってこられない。"
  "<b>自分が1日に何度も繰り返している操作に気づき、それを楽にする手段を notes/ に書き留める</b> — "
  "この堆積こそが、君だけの差別化された研究環境になる。"
  "今日その第一層として、ノートブックという道具の「未読マニュアル」を一冊読み終えた。")

# ===================== ビルド =====================
doc = SimpleDocTemplate(
    "notebooks_jupyter_vs_marimo.pdf", pagesize=A4,
    topMargin=20*mm, bottomMargin=18*mm, leftMargin=20*mm, rightMargin=20*mm,
    title="ノートブック実験環境 入門", author="complex_systems",
)

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("JP", 8)
    canvas.setFillColor(colors.HexColor("#8a939c"))
    canvas.drawCentredString(A4[0] / 2, 10*mm,
                             "complex_systems 講義資料 #01  —  %d" % doc.page)
    canvas.restoreState()

doc.build(story, onFirstPage=lambda c, d: None, onLaterPages=footer)
print("wrote notebooks_jupyter_vs_marimo.pdf")
