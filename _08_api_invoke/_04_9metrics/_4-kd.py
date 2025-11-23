import glob

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ===============================
# 1. 计算 Stochastic KD
# ===============================
def compute_kd(df, n=9, k_smooth=3, d_smooth=3):
    df = df.copy()

    # 如果没有 high/low，用 close 模拟（不如真实数据准确）
    if "high" not in df.columns:
        df["high"] = df["close"]
    if "low" not in df.columns:
        df["low"] = df["close"]

    low_n = df["low"].rolling(n).min()
    high_n = df["high"].rolling(n).max()

    # K% (未平滑)
    rsv = (df["close"] - low_n) / (high_n - low_n) * 100

    df["K"] = rsv.rolling(k_smooth).mean()
    df["D"] = df["K"].rolling(d_smooth).mean()

    return df

# ===============================
# 2. KD 背离检测（价格 vs K）
# ===============================
def detect_kd_divergence(df, window=5):
    bullish = []
    bearish = []

    for i in range(window, len(df)):

        # ----------- 看涨背离（价格创新低，KD 没创新低） -----------
        price_low_now = df["close"].iloc[i]
        price_low_prev = df["close"].iloc[i-window]

        k_now = df["K"].iloc[i]
        k_prev = df["K"].iloc[i-window]

        if price_low_now < price_low_prev and k_now > k_prev:
            bullish.append(i)

        # ----------- 看跌背离（价格创新高，KD 没创新高） -----------
        price_high_now = df["close"].iloc[i]
        price_high_prev = df["close"].iloc[i-window]

        if price_high_now > price_high_prev and k_now < k_prev:
            bearish.append(i)

    return bullish, bearish

# ===============================
# 3. 图形展示（价格 + KD + 背离箭头）
# ===============================
def plot_kd_divergence(df, bullish, bearish):
    fig = plt.figure(figsize=(16, 10))

    # ----------- Price Chart ----------------
    ax1 = plt.subplot(2, 1, 1)
    ax1.set_title("Close Price + KD Divergence")

    ax1.plot(df["date"], df["close"], label="close", linewidth=1.2)

    ax1.scatter(df["date"].iloc[bullish], df["close"].iloc[bullish],
                marker="^", color="green", s=80, label="Bullish Div")

    ax1.scatter(df["date"].iloc[bearish], df["close"].iloc[bearish],
                marker="v", color="red", s=80, label="Bearish Div")

    ax1.legend()

    # ----------- KD Chart ----------------
    ax2 = plt.subplot(2, 1, 2)
    ax2.set_title("Stochastic K / D")

    ax2.plot(df["date"], df["K"], label="K", linewidth=1.2)
    ax2.plot(df["date"], df["D"], label="D", linewidth=1.2)

    ax2.axhline(20, linestyle="--", color="gray")  # 超卖
    ax2.axhline(80, linestyle="--", color="gray")  # 超买

    ax2.scatter(df["date"].iloc[bullish], df["K"].iloc[bullish],
                color="green", s=60)
    ax2.scatter(df["date"].iloc[bearish], df["K"].iloc[bearish],
                color="red", s=60)

    ax2.legend()

    plt.tight_layout()
    plt.show()


# =============================================
# 使用方法
# =============================================
# df = pd.read_csv(glob.glob("../output/price/2025/qqq/part-00000-*-c000.csv")[0])
# df = pd.read_csv(glob.glob("../output/price/2025/iren/part-00000-*-c000.csv")[0])
# df = pd.read_csv(glob.glob("../output/price/2024/iren/part-00000-*-c000.csv")[0])
# df = pd.read_csv(glob.glob("../output/price/2023/iren/part-00000-*-c000.csv")[0])
# df = pd.read_csv(glob.glob("../output/price/2022/iren/part-00000-*-c000.csv")[0])
# df = pd.read_csv(glob.glob("../output/price/2025/amd/part-00000-*-c000.csv")[0])
df = pd.read_csv(glob.glob("../output/price/2025/nbis/part-00000-*-c000.csv")[0])
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


# df = pd.read_csv("your_data.csv")  # 必须含 date, close；可选 high, low
df["date"] = pd.to_datetime(df["date"])

df = compute_kd(df)
bullish, bearish = detect_kd_divergence(df, window=5)
plot_kd_divergence(df, bullish, bearish)
