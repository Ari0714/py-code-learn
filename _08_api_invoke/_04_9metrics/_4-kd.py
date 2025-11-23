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
# df = pd.read_csv("output/price/2025/iren/part-00000-0571651a-cd11-44f0-9fb4-98b9a773fab1-c000.csv") # 必须含 columns: date, close
# df = pd.read_csv("output/price/2024/iren/part-00000-5fd6f3a8-d1a0-447d-a180-dd283881b273-c000.csv")
# df = pd.read_csv("output/price/2023/iren/part-00000-be9200bb-ba07-4c24-92ca-5b746bfa4e83-c000.csv")

# df = pd.read_csv("output/price/2025/cifr/part-00000-9caee7f6-139e-4699-a210-58313d297c35-c000.csv") # 必须含 columns: date, close
# df = pd.read_csv("output/price/2025/amd/part-00000-ab93d9be-aef3-4fdd-83f2-7041b83cd1ba-c000.csv")
df = pd.read_csv("../output/price/2025/ONDS/part-00000-c40db715-98f1-48f9-bb09-570998337230-c000.csv")
# df = pd.read_csv("output/price/2025/nbis/part-00000-4ad7dc75-8b5b-4230-b817-3a6fa4f055f6-c000.csv")
# df = pd.read_csv("output/price/2025/hood/part-00000-d7300028-1aaa-4676-b0f9-cd767bb91778-c000.csv")
# df = pd.read_csv("output/price/2025/qqq/part-00000-172e26f4-06a1-4cb4-8f09-25bf18021637-c000.csv")
# df = pd.read_csv("output/price/2025/sndk/part-00000-702568f6-1309-4bad-9767-591c08617dec-c000.csv")
# df = pd.read_csv("output/price/2025/app/part-00000-69e853a3-756a-47e0-9533-a674250f06d9-c000.csv")
# df = pd.read_csv("output/price/2025/crdo/part-00000-4fb0bb26-812e-47a3-9fde-3fcafeeaa611-c000.csv")



# df = pd.read_csv("your_data.csv")  # 必须含 date, close；可选 high, low
df["date"] = pd.to_datetime(df["date"])

df = compute_kd(df)
bullish, bearish = detect_kd_divergence(df, window=5)
plot_kd_divergence(df, bullish, bearish)
