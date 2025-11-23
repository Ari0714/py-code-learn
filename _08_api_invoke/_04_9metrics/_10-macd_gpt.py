import glob

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ========= MACD =========
def calc_macd(close, short=12, long=26, signal=9):
    ema_short = close.ewm(span=short, adjust=False).mean()
    ema_long = close.ewm(span=long, adjust=False).mean()
    diff = ema_short - ema_long
    dea = diff.ewm(span=signal, adjust=False).mean()
    macd = (diff - dea) * 2
    return diff, dea, macd


# ========= 找局部高低点 =========
def find_local_extrema(series, window=2):
    lows = []
    highs = []
    for i in range(window, len(series)-window):
        if series[i] == min(series[i-window:i+window+1]):
            lows.append(i)
        if series[i] == max(series[i-window:i+window+1]):
            highs.append(i)
    return lows, highs


# ========= MACD 背离检测 =========
def detect_macd_divergence(df):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    # MACD
    df["diff"], df["dea"], df["macd"] = calc_macd(df["close"])

    # 局部高低点（价格 & diff）
    price_lows, price_highs = find_local_extrema(df["close"])
    diff_lows, diff_highs = find_local_extrema(df["diff"])

    bullish = []  # 看涨背离
    bearish = []  # 看跌背离

    # ---- 看涨 (价格新低 + diff不新低) ----
    for i in range(1, len(price_lows)):
        p1, p2 = price_lows[i-1], price_lows[i]
        if df["close"].iloc[p2] < df["close"].iloc[p1] and df["diff"].iloc[p2] > df["diff"].iloc[p1]:
            bullish.append(p2)

    # ---- 看跌 (价格新高 + diff不新高) ----
    for i in range(1, len(price_highs)):
        p1, p2 = price_highs[i-1], price_highs[i]
        if df["close"].iloc[p2] > df["close"].iloc[p1] and df["diff"].iloc[p2] < df["diff"].iloc[p1]:
            bearish.append(p2)

    return bullish, bearish, df


# ========= 绘图 =========
def plot_macd_divergence(df, bullish, bearish):

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    fig = plt.figure(figsize=(15, 10))

    # ====== Price 图 ======
    ax1 = plt.subplot(2, 1, 1)
    ax1.plot(df["date"], df["close"], label="Close Price")
    ax1.set_title("Close Price + MACD Divergence")

    # 看涨背离（绿色 ↑）
    ax1.scatter(df["date"].iloc[bullish], df["close"].iloc[bullish],
                color="green", s=80, marker="^", label="Bullish Divergence")

    # 看跌背离（红色 ↓）
    ax1.scatter(df["date"].iloc[bearish], df["close"].iloc[bearish],
                color="red", s=80, marker="v", label="Bearish Divergence")

    ax1.legend()

    # ====== MACD 图 ======
    ax2 = plt.subplot(2, 1, 2)
    ax2.set_title("MACD (DIFF / DEA / Histogram)")

    ax2.plot(df["date"], df["diff"], label="DIFF")
    ax2.plot(df["date"], df["dea"], label="DEA")

    # MACD 柱状图
    ax2.bar(df["date"], df["macd"], width=1, color=["red" if x < 0 else "green" for x in df["macd"]])

    # 背离点
    ax2.scatter(df["date"].iloc[bullish], df["diff"].iloc[bullish],
                color="green", s=60)
    ax2.scatter(df["date"].iloc[bearish], df["diff"].iloc[bearish],
                color="red", s=60)

    ax2.legend()

    plt.tight_layout()
    plt.show()


# ========= 主函数 =========
def detect_and_plot_macd(df):
    bullish, bearish, df2 = detect_macd_divergence(df)
    plot_macd_divergence(df2, bullish, bearish)
    return bullish, bearish, df2


if __name__ == '__main__':
    # df = pd.read_csv(glob.glob("../output/price/2025/qqq/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/iren/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2024/iren/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2023/iren/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2022/iren/part-00000-*-c000.csv")[0])
    df = pd.read_csv(glob.glob("../output/price/2025/amd/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/nbis/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/cifr/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/wulf/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/onds/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2024/onds/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/oklo/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/avgo/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2024/avgo/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2023/avgo/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/tsla/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/nvda/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2022/amd/part-00000-*-c000.csv")[0])

    bullish, bearish, df2 = detect_and_plot_macd(df)
