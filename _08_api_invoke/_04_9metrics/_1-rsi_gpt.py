import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import glob

def compute_rsi(close, period=14):
    delta = close.diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    gain_ema = pd.Series(gain).ewm(span=period, adjust=False).mean()
    loss_ema = pd.Series(loss).ewm(span=period, adjust=False).mean()

    rsi = 100 - (100 / (1 + gain_ema / loss_ema))
    return rsi


# -------------------- 背离检测 (价格+RSI) --------------------
def find_divergence(df, rsi_period=14, window=5):
    df = df.copy()
    df["rsi"] = compute_rsi(df["close"], rsi_period)

    # 局部低点 / 高点 (基于 close)
    df["low"] = df["close"].rolling(window, center=True).apply(lambda x: x.argmin(), raw=True)
    df["high"] = df["close"].rolling(window, center=True).apply(lambda x: x.argmax(), raw=True)

    bullish = []
    bearish = []

    for i in range(window, len(df) - window):

        # ---- 看涨背离 (价格LL, RSI HL) ----
        if df["low"].iloc[i] == window // 2:
            prev = df.iloc[:i]
            prev = prev[prev["low"] == window // 2]
            if len(prev) > 0:
                j = prev.index[-1]
                price_ll = df["close"].iloc[i] < df["close"].iloc[j]
                rsi_hl = df["rsi"].iloc[i] > df["rsi"].iloc[j]
                if price_ll and rsi_hl:
                    bullish.append(i)

        # ---- 看跌背离 (价格HH, RSI LH) ----
        if df["high"].iloc[i] == window // 2:
            prev = df.iloc[:i]
            prev = prev[prev["high"] == window // 2]
            if len(prev) > 0:
                j = prev.index[-1]
                price_hh = df["close"].iloc[i] > df["close"].iloc[j]
                rsi_lh = df["rsi"].iloc[i] < df["rsi"].iloc[j]
                if price_hh and rsi_lh:
                    bearish.append(i)

    return bullish, bearish, df


# -------------------- 绘图：收盘价折线图 + RSI + 背离箭头 --------------------
import matplotlib.pyplot as plt
import mplcursors

def plot_divergence(df, bullish, bearish):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    fig = plt.figure(figsize=(16, 10))

    # ====== Price ======
    ax1 = plt.subplot(2, 1, 1)
    ax1.set_title("Close Price + Divergence")

    # 主价格线：绑定真实 index
    line_price, = ax1.plot(df["date"], df["close"], label="close")
    line_price._df_index = df.index.to_numpy()

    # 看涨背离
    bull_idx = df.index.to_numpy()[bullish]
    bull_scatter = ax1.scatter(df["date"].iloc[bullish], df["close"].iloc[bullish],
                               color="green", s=80, marker="^")
    bull_scatter._df_index = bull_idx

    # 看跌背离
    bear_idx = df.index.to_numpy()[bearish]
    bear_scatter = ax1.scatter(df["date"].iloc[bearish], df["close"].iloc[bearish],
                               color="red", s=80, marker="v")
    bear_scatter._df_index = bear_idx
    ax1.legend()

    # ====== RSI ======
    ax2 = plt.subplot(2, 1, 2)
    ax2.set_title("RSI + Divergence")

    line_rsi, = ax2.plot(df["date"], df["rsi"], label="RSI")
    line_rsi._df_index = df.index.to_numpy()

    # 添加30/70虚线
    ax2.axhline(30, color="gray", linestyle="--", linewidth=1)
    ax2.axhline(70, color="gray", linestyle="--", linewidth=1)

    bull_rsi = ax2.scatter(df["date"].iloc[bullish], df["rsi"].iloc[bullish],
                           color="green", s=60)
    bull_rsi._df_index = bull_idx

    bear_rsi = ax2.scatter(df["date"].iloc[bearish], df["rsi"].iloc[bearish],
                           color="red", s=60)
    bear_rsi._df_index = bear_idx
    ax2.legend()

    # ====== Hover ============
    cursor = mplcursors.cursor([line_price, line_rsi,
                                bull_scatter, bear_scatter,
                                bull_rsi, bear_rsi], hover=True)

    @cursor.connect("add")
    def on_add(sel):
        artist = sel.artist

        # 使用艺术家中存的真实 index → 100% 正确日期
        true_idx = artist._df_index[sel.index]

        row = df.loc[true_idx]
        date = row["date"].strftime("%Y-%m-%d")

        label = ""
        if true_idx in bullish:
            label = "Bullish Divergence"
        elif true_idx in bearish:
            label = "Bearish Divergence"

        sel.annotation.set(
            text=f"{date}\nClose: {row['close']:.2f}\nRSI: {row['rsi']:.2f}\n{label}",
            fontsize=9
        )

    plt.tight_layout()
    plt.show()



# ------------------- 使用示例 -------------------
#2025
voo5 = glob.glob("../output/price/2025/voo/part-00000-*-c000.csv")[0]
qqq5 = glob.glob("../output/price/2025/qqq/part-00000-*-c000.csv")[0]

iren5 = glob.glob("../output/price/2025/iren/part-00000-*-c000.csv")[0]  #lookback 5 - 13
nbis5 = glob.glob("../output/price/2025/nbis/part-00000-*-c000.csv")[0]
cifr5 = glob.glob("../output/price/2025/cifr/part-00000-*-c000.csv")[0]
crwv5 = glob.glob("../output/price/2025/crwv/part-00000-*-c000.csv")[0]
wulf5 = glob.glob("../output/price/2025/wulf/part-00000-*-c000.csv")[0]

rklb5 = glob.glob("../output/price/2025/rklb/part-00000-*-c000.csv")[0]
asts5 = glob.glob("../output/price/2025/asts/part-00000-*-c000.csv")[0]
onds5 = glob.glob("../output/price/2025/onds/part-00000-*-c000.csv")[0]

nvda5 = glob.glob("../output/price/2025/nvda/part-00000-*-c000.csv")[0]
goog5 = glob.glob("../output/price/2025/goog/part-00000-*-c000.csv")[0]
tsla5 = glob.glob("../output/price/2025/tsla/part-00000-*-c000.csv")[0]
# aapl5 = glob.glob("../output/price/2025/aapl/part-00000-*-c000.csv")[0]
# meta5 = glob.glob("../output/price/2025/meta/part-00000-*-c000.csv")[0]

amd5 = glob.glob("../output/price/2025/amd/part-00000-*-c000.csv")[0]
tsm5 = glob.glob("../output/price/2025/tsm/part-00000-*-c000.csv")[0]
avgo5 = glob.glob("../output/price/2025/avgo/part-00000-*-c000.csv")[0]

be5 = glob.glob("../output/price/2025/be/part-00000-*-c000.csv")[0]
eose5 = glob.glob("../output/price/2025/eose/part-00000-*-c000.csv")[0]
oklo5 = glob.glob("../output/price/2025/oklo/part-00000-*-c000.csv")[0]
mp5 = glob.glob("../output/price/2025/mp/part-00000-*-c000.csv")[0]

hood5 = glob.glob("../output/price/2025/hood/part-00000-*-c000.csv")[0]
pltr5 = glob.glob("../output/price/2025/pltr/part-00000-*-c000.csv")[0]

ibit5 = glob.glob("../output/price/2025/ibit/part-00000-*-c000.csv")[0]

sndk5 = glob.glob("../output/price/2025/sndk/part-00000-*-c000.csv")[0]

app5 = glob.glob("../output/price/2025/app/part-00000-*-c000.csv")[0]

crdo5 = glob.glob("../output/price/2025/crdo/part-00000-*-c000.csv")[0]


df = pd.read_csv(cifr5)
bullish, bearish, df = find_divergence(df)
plot_divergence(df, bullish, bearish)


# 2024
voo4 = "VOO/part-00000-1235e567-30cf-41ee-9d40-6152681ac389-c000.csv"
qqq4 = "QQQ/part-00000-0cb8de97-007b-48f6-86b7-cd7d5e7fd46e-c000.csv"

iren4 = "IREN/part-00000-5fd6f3a8-d1a0-447d-a180-dd283881b273-c000.csv"  #lookback 5 - 13
nbis4 = "nbis/part-00000-2e763d64-12cc-4a4d-b41a-94c5e75d8403-c000.csv"
cifr4 = "cifr/part-00000-d72ff08e-1480-4896-8845-00f82335811d-c000.csv"
crwv4 = "CRWV/"
wulf4 = "WULF/part-00000-2f16989b-2921-4277-a9ce-0c380fbb169c-c000.csv"

rklb4 = "RKLB/part-00000-06100147-b401-43c2-8378-d22447fad4e2-c000.csv"
onds4 = "ONDS/part-00000-321ce7c0-84a5-4a09-9f94-0dcff0c5b471-c000.csv"

nvda4 = "NVDA/part-00000-b6b363d6-3242-4a3e-801b-274a6ed442d7-c000.csv"
goog4 = "GOOG/part-00000-d1b20e11-5305-4eaa-9105-bdde04ec9d12-c000.csv"
tsla4 = "TSLA/part-00000-4f753a2a-0492-454d-817d-2d4bf412c629-c000.csv"

amd4 = "AMD/part-00000-06cc86c0-e626-4a3f-a7c5-2b14a6d9c7d4-c000.csv"
tsm4 = "TSM/part-00000-4fc564e2-f497-4122-b35d-bcfdc94263b1-c000.csv"
avgo4 = "AVGO/part-00000-3b436a51-4a2d-4c59-b18b-a118f2d14212-c000.csv"

be4 = "BE/part-00000-7cb10b4b-4353-4423-aa7f-8e82bea6eae7-c000.csv"
eose4 = "EOSE/part-00000-d5e0c71f-f3c1-45c6-a88e-097803e2a038-c000.csv"

hood4 = "HOOD/part-00000-9eabae27-65bc-4d37-8e00-7af051e287d3-c000.csv"
pltr4 = "PLTR/part-00000-a508e3c4-a3e4-4efd-a806-727dcc1b35f0-c000.csv"

# df = pd.read_csv(f'output/price/2024/{iren4}')
# bullish, bearish, df = find_divergence(df)
# plot_divergence(df, bullish, bearish)


# 2023
voo3 = "VOO/part-00000-181c18ff-cfe4-4d57-90fb-54b14914d003-c000.csv"
qqq3 = "QQQ/part-00000-8f954279-09b4-49ed-b85b-455ce9c47b0e-c000.csv"

iren3 = "IREN/part-00000-be9200bb-ba07-4c24-92ca-5b746bfa4e83-c000.csv"  #lookback 5 - 13
nbis3 = "nbis/"
cifr3 = "cifr/part-00000-f35ee017-4062-4b37-b850-64974c9f5fc6-c000.csv"
crwv3 = "CRWV/"
wulf3 = "WULF/part-00000-b624c3ff-5231-4e18-85d0-270474ae7214-c000.csv"

rklb3 = "RKLB/part-00000-1bb288dd-6a2e-4536-a12b-50b5eb0d064b-c000.csv"
onds3 = "ONDS/part-00000-e777c634-6f25-461c-8e73-eb6fcec4cd92-c000.csv"

nvda3 = "NVDA/part-00000-9e9d9051-cb8c-4e45-8ed2-185c2c61d4a0-c000.csv"
goog3 = "GOOG/part-00000-97375ed0-abc3-4ea2-b66b-7934a4058215-c000.csv"
tsla3 = "TSLA/part-00000-872f8dbd-9934-4198-b8db-aba8ee819f3a-c000.csv"

amd3 = "AMD/part-00000-ac684a32-10d5-45a7-b7ee-3d4f73308151-c000.csv"
tsm3 = "TSM/part-00000-3e30a0f8-7e58-4d0b-a901-4a237c2f9a11-c000.csv"
avgo3 = "AVGO/part-00000-f889a19b-c8e3-40cc-a9cd-50c8963332ba-c000.csv"

be3 = "BE/part-00000-f6351cbb-2c07-41bb-add9-9c6755577310-c000.csv"
eose3 = "EOSE/part-00000-9f43e548-e614-4f44-b005-f000c947597e-c000.csv"

hood3 = "HOOD/part-00000-7564dddb-31f9-4fbc-8aae-9ca4afb304f1-c000.csv"
pltr3 = "PLTR/part-00000-0001dff1-ef5c-4301-af6e-aca4cfca1447-c000.csv"

# df = pd.read_csv(f'output/price/2023/{iren3}')
# bullish, bearish, df = find_divergence(df)
# plot_divergence(df, bullish, bearish)
