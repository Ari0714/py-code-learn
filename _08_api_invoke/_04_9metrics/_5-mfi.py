import glob

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ===================================================
# 1️⃣ 计算 MFI（资金流量指数）
# ===================================================
def compute_mfi(df, n=14):
    df = df.copy()

    # 必须有成交量字段
    if "volume" not in df.columns:
        raise ValueError("MFI 必须包含 volume 字段")

    # 若缺 high/low，用 close 模拟（精度差一些）
    if "high" not in df.columns:
        df["high"] = df["close"]
    if "low" not in df.columns:
        df["low"] = df["close"]

    # 典型价格（TP）
    tp = (df["high"] + df["low"] + df["close"]) / 3

    # 原始资金流（Raw Money Flow）
    rmf = tp * df["volume"]

    # 正资金流 / 负资金流
    positive_flow = []
    negative_flow = []

    for i in range(1, len(df)):
        if tp.iloc[i] > tp.iloc[i-1]:
            positive_flow.append(rmf.iloc[i])
            negative_flow.append(0)
        else:
            positive_flow.append(0)
            negative_flow.append(rmf.iloc[i])

    positive_flow = pd.Series(positive_flow)
    negative_flow = pd.Series(negative_flow)

    # 加回第一行
    positive_flow = pd.concat([pd.Series([0]), positive_flow], ignore_index=True)
    negative_flow = pd.concat([pd.Series([0]), negative_flow], ignore_index=True)

    # N 天正/负资金流
    pos_n = positive_flow.rolling(n).sum()
    neg_n = negative_flow.rolling(n).sum()

    # MFI
    mfi = 100 - (100 / (1 + pos_n / neg_n))
    df["MFI"] = mfi

    return df

# ===================================================
# 2️⃣ 检测 MFI 背离
# ===================================================
def detect_mfi_divergence(df, window=5):
    bullish = []
    bearish = []

    for i in range(window, len(df)):

        # ----------- 看涨背离（价格创新低，MFI 没创新低）-----------
        if df["close"].iloc[i] < df["close"].iloc[i - window] and \
           df["MFI"].iloc[i] > df["MFI"].iloc[i - window]:
            bullish.append(i)

        # ----------- 看跌背离（价格创新高，MFI 没创新高）-----------
        if df["close"].iloc[i] > df["close"].iloc[i - window] and \
           df["MFI"].iloc[i] < df["MFI"].iloc[i - window]:
            bearish.append(i)

    return bullish, bearish


# ===================================================
# 3️⃣ 图形展示（价格 + MFI + 背离箭头）
# ===================================================
def plot_mfi_divergence(df, bullish, bearish):
    fig = plt.figure(figsize=(16, 10))

    # -------- Price 图 ----------
    ax1 = plt.subplot(2, 1, 1)
    ax1.set_title("Price + MFI Divergence")

    ax1.plot(df["date"], df["close"], label="Close", linewidth=1.2)

    ax1.scatter(df["date"].iloc[bullish], df["close"].iloc[bullish],
                color="green", marker="^", s=80, label="Bullish Div")

    ax1.scatter(df["date"].iloc[bearish], df["close"].iloc[bearish],
                color="red", marker="v", s=80, label="Bearish Div")

    ax1.legend()

    # -------- MFI 图 ----------
    ax2 = plt.subplot(2, 1, 2)
    ax2.set_title("MFI")

    ax2.plot(df["date"], df["MFI"], label="MFI", linewidth=1.2)

    # 超买超卖区（常用）
    ax2.axhline(80, linestyle="--", color="gray")   # 超买
    ax2.axhline(20, linestyle="--", color="gray")   # 超卖

    ax2.scatter(df["date"].iloc[bullish], df["MFI"].iloc[bullish],
                color="green", s=60)
    ax2.scatter(df["date"].iloc[bearish], df["MFI"].iloc[bearish],
                color="red", s=60)

    ax2.legend()

    plt.tight_layout()
    plt.show()


# ===================================================
# 使用方法
# ===================================================
# df = pd.read_csv(glob.glob("../output/price/2025/qqq/part-00000-*-c000.csv")[0])
df = pd.read_csv(glob.glob("../output/price/2025/iren/part-00000-*-c000.csv")[0])
# df = pd.read_csv(glob.glob("../output/price/2024/iren/part-00000-*-c000.csv")[0])
# df = pd.read_csv(glob.glob("../output/price/2023/iren/part-00000-*-c000.csv")[0])
# df = pd.read_csv(glob.glob("../output/price/2022/iren/part-00000-*-c000.csv")[0])
# df = pd.read_csv(glob.glob("../output/price/2025/amd/part-00000-*-c000.csv")[0])
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


# df = pd.read_csv("your_data.csv")
df["date"] = pd.to_datetime(df["date"])

df = compute_mfi(df)
bullish, bearish = detect_mfi_divergence(df, window=5)
plot_mfi_divergence(df, bullish, bearish)
