import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
# df = pd.read_csv("output/price/2025/iren/part-00000-0571651a-cd11-44f0-9fb4-98b9a773fab1-c000.csv")  # 必须含 columns: date, close
# df = pd.read_csv("output/price/2024/iren/part-00000-5fd6f3a8-d1a0-447d-a180-dd283881b273-c000.csv")
# df = pd.read_csv("output/price/2023/iren/part-00000-be9200bb-ba07-4c24-92ca-5b746bfa4e83-c000.csv")

# df = pd.read_csv("output/price/2025/cifr/part-00000-9caee7f6-139e-4699-a210-58313d297c35-c000.csv") # 必须含 columns: date, close
# df = pd.read_csv("output/price/2025/amd/part-00000-ab93d9be-aef3-4fdd-83f2-7041b83cd1ba-c000.csv")
# df = pd.read_csv("output/price/2025/onds/part-00000-c40db715-98f1-48f9-bb09-570998337230-c000.csv")
# df = pd.read_csv("output/price/2025/nbis/part-00000-4ad7dc75-8b5b-4230-b817-3a6fa4f055f6-c000.csv")
# df = pd.read_csv("output/price/2025/hood/part-00000-d7300028-1aaa-4676-b0f9-cd767bb91778-c000.csv")
# df = pd.read_csv("output/price/2025/qqq/part-00000-172e26f4-06a1-4cb4-8f09-25bf18021637-c000.csv")
df = pd.read_csv("output/price/2025/sndk/part-00000-702568f6-1309-4bad-9767-591c08617dec-c000.csv")
# df = pd.read_csv("output/price/2025/app/part-00000-69e853a3-756a-47e0-9533-a674250f06d9-c000.csv")
# df = pd.read_csv("output/price/2025/crdo/part-00000-4fb0bb26-812e-47a3-9fde-3fcafeeaa611-c000.csv")


# df = pd.read_csv("your_data.csv")  # 必须含 date, close，最好含 high, low
df["date"] = pd.to_datetime(df["date"])

df = compute_cci(df)
bullish, bearish = detect_cci_divergence(df, window=5)
plot_cci_divergence(df, bullish, bearish)
