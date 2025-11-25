import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

# ===================================================
# 1️⃣ 计算 CCI（顺势指标）
# ===================================================
def compute_cci(df, n=20, c=0.015):
    df = df.copy()

    # 如果缺 high / low，用 close 模拟（准确性差一些）
    if "high" not in df.columns:
        df["high"] = df["close"]
    if "low" not in df.columns:
        df["low"] = df["close"]

    # 典型价格（TP）
    tp = (df["high"] + df["low"] + df["close"]) / 3

    ma = tp.rolling(n).mean()
    md = (tp - ma).abs().rolling(n).mean()

    df["CCI"] = (tp - ma) / (c * md)
    return df

# ===================================================
# 2️⃣ 检测 CCI 背离：价格 vs CCI（window 后看）
# ===================================================
def detect_cci_divergence(df, window=5):
    bullish = []
    bearish = []

    for i in range(window, len(df)):

        # ----------- 看涨背离（价格创新低，CCI 没创新低）-----------
        price_now = df["close"].iloc[i]
        price_prev = df["close"].iloc[i - window]

        cci_now = df["CCI"].iloc[i]
        cci_prev = df["CCI"].iloc[i - window]

        if price_now < price_prev and cci_now > cci_prev:
            bullish.append(i)

        # ----------- 看跌背离（价格创新高，CCI 没创新高）-----------
        if price_now > price_prev and cci_now < cci_prev:
            bearish.append(i)

    return bullish, bearish

# ===================================================
# 3️⃣ 图形展示（价格 + CCI + 背离箭头）
# ===================================================
def plot_cci_divergence(df, bullish, bearish):
    fig = plt.figure(figsize=(16, 10))

    # -------- Price Chart ----------
    ax1 = plt.subplot(2, 1, 1)
    ax1.set_title("Close Price + CCI Divergence")

    ax1.plot(df["date"], df["close"], label="close", linewidth=1.2)

    ax1.scatter(df["date"].iloc[bullish], df["close"].iloc[bullish],
                marker="^", color="green", s=80, label="Bullish Div")

    ax1.scatter(df["date"].iloc[bearish], df["close"].iloc[bearish],
                marker="v", color="red", s=80, label="Bearish Div")

    ax1.legend()

    # -------- CCI Chart ----------
    ax2 = plt.subplot(2, 1, 2)
    ax2.set_title("Commodity Channel Index (CCI)")

    ax2.plot(df["date"], df["CCI"], label="CCI", linewidth=1.2)

    # 常用 CCI 参考线
    ax2.axhline(100, linestyle="--", color="gray")
    ax2.axhline(-100, linestyle="--", color="gray")

    ax2.scatter(df["date"].iloc[bullish], df["CCI"].iloc[bullish],
                color="green", s=60)
    ax2.scatter(df["date"].iloc[bearish], df["CCI"].iloc[bearish],
                color="red", s=60)

    ax2.legend()
    plt.tight_layout()
    plt.show()


# ===================================================
# 使用方法
# ===================================================
# df = pd.read_csv(glob.glob("../output/price/2025/qqq/part-00000-*-c000.csv")[0])
# df = pd.read_csv(glob.glob("../output/price/2025/iren/part-00000-*-c000.csv")[0])
# df = pd.read_csv(glob.glob("../output/price/2024/iren/part-00000-*-c000.csv")[0])
# df = pd.read_csv(glob.glob("../output/price/2023/iren/part-00000-*-c000.csv")[0])
# df = pd.read_csv(glob.glob("../output/price/2022/iren/part-00000-*-c000.csv")[0])
# df = pd.read_csv(glob.glob("../output/price/2025/amd/part-00000-*-c000.csv")[0])
df = pd.read_csv(glob.glob("../output/price/2025/2025-11-24/nbis/part-00000-*-c000.csv")[0])
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

# df = pd.read_csv("your_data.csv")  # 必须含 date, close，最好含 high, low
df["date"] = pd.to_datetime(df["date"])

df = compute_cci(df)
bullish, bearish = detect_cci_divergence(df, window=5)
plot_cci_divergence(df, bullish, bearish)
