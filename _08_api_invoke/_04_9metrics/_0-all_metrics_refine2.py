import glob

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplcursors


# =========================================
# 1. 构造 high/low（无未来数据）
# =========================================
def add_synthetic_high_low(df, pct=0.002):
    df = df.copy()
    base_high = df[["open", "close"]].max(axis=1)
    base_low = df[["open", "close"]].min(axis=1)
    df["high"] = base_high * (1 + pct)
    df["low"] = base_low * (1 - pct)
    return df

# def add_synthetic_high_low(df, pct=0.002):
#     # df = df.copy()
#     # base_high = df[["open", "close"]].max(axis=1)
#     # base_low = df[["open", "close"]].min(axis=1)
#     # df["high"] = base_high * (1 + pct)
#     # df["low"] = base_low * (1 - pct)
#     return df

# =========================================
# 2. 各指标计算
# =========================================

def calc_rsi(close, n=14):
    delta = close.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    ma_up = up.rolling(n).mean()
    ma_down = down.rolling(n).mean()
    return 100 - 100 / (1 + ma_up / (ma_down + 1e-9))

def calc_bollinger_pctb(close, n=20, k=2):
    ma = close.rolling(n).mean()
    std = close.rolling(n).std()
    upper = ma + k * std
    lower = ma - k * std
    return (close - lower) / (upper - lower + 1e-9)

def calc_kd(df, n=9):
    low_n = df["low"].rolling(n).min()
    high_n = df["high"].rolling(n).max()
    rsv = (df["close"] - low_n) / (high_n - low_n + 1e-9) * 100
    K = rsv.ewm(alpha=1/3).mean()
    D = K.ewm(alpha=1/3).mean()
    return K, D

def calc_cci(df, n=20):
    tp = (df["high"] + df["low"] + df["close"]) / 3
    ma = tp.rolling(n).mean()
    md = (tp - ma).abs().rolling(n).mean()
    return (tp - ma) / (0.015 * (md + 1e-9))

def calc_mfi(df, n=14):
    tp = (df["high"] + df["low"] + df["close"]) / 3
    mf = tp * df["volume"]
    pos = mf.where(tp > tp.shift(), 0)
    neg = mf.where(tp < tp.shift(), 0)
    pos_sum = pos.rolling(n).sum()
    neg_sum = neg.rolling(n).sum()
    return 100 - 100 / (1 + pos_sum / (neg_sum + 1e-9))


# =========================================
# 3. 检测拐点（所有指标都要显示）
# =========================================
def detect_all_signals(df):
    df = df.copy()
    df = add_synthetic_high_low(df)

    df["rsi"] = calc_rsi(df["close"])
    df["pctB"] = calc_bollinger_pctb(df["close"])
    df["K"], df["D"] = calc_kd(df)
    df["cci"] = calc_cci(df)
    df["mfi"] = calc_mfi(df)

    signals = []

    for i in range(1, len(df)):

        ### 底部指标
        bottom = {
            "RSI": df["rsi"].iloc[i] < 30,
            "%B": df["pctB"].iloc[i-1] < 0 and df["pctB"].iloc[i] > 0.05,
            "KD": (df["K"].iloc[i] < 20 and df["D"].iloc[i] < 20),
            "CCI": df["cci"].iloc[i] < -100,
            "MFI": df["mfi"].iloc[i] < 20
        }

        ### 顶部指标
        top = {
            "RSI": df["rsi"].iloc[i] > 70,
            "%B": df["pctB"].iloc[i-1] > 1 and df["pctB"].iloc[i] < 0.95,
            "KD": (df["K"].iloc[i] > 80 and df["D"].iloc[i] > 80),
            "CCI": df["cci"].iloc[i] > 100,
            "MFI": df["mfi"].iloc[i] > 80
        }

        bottom_hits = [k for k, v in bottom.items() if v]
        top_hits = [k for k, v in top.items() if v]

        # 所有指标都要显示
        if bottom_hits:
            signals.append((i, "bottom", bottom_hits))

        if top_hits:
            signals.append((i, "top", top_hits))

    return signals, df


# =========================================
# 4. 图形绘制 + Hover 显示所有信息
# =========================================
def plot_signals(df, signals):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    fig, ax = plt.subplots(figsize=(16, 8))

    # 主线
    ax.plot(df["date"], df["close"], label="Close", lw=1.2)

    points = []
    meta = []   # 用来存储 hover 信息

    for idx, sig_type, names in signals:

        # =============== Strong 信号（ >=2 指标 ) ==================
        strong = len(names) >= 2

        if strong:
            if sig_type == "bottom":
                color = "green"  # 金色星星（Strong Bull）
                marker = "*"
                size = 220
            else:
                color = "red"  # 绿色星星（Strong Bear）
                marker = "*"
                size = 220
        else:
            # =============== 普通信号圆点 ==================
            if sig_type == "bottom":
                color = "green"
            else:
                color = "red"
            marker = "o"
            size = 120

        scat = ax.scatter(
            df["date"].iloc[idx],
            df["close"].iloc[idx],
            color=color,
            s=size,
            marker=marker
        )

        scat._meta = {
            "idx": idx,
            "type": sig_type,
            "names": names,
            "strong": strong,
        }

        points.append(scat)

    # Hover 展示
    cursor = mplcursors.cursor(points, hover=True)

    @cursor.connect("add")
    def on_hover(sel):
        m = sel.artist._meta
        i = m["idx"]
        row = df.iloc[i]

        text = (
            f"{row['date'].strftime('%Y-%m-%d')}\n"
            f"Type: {m['type'].capitalize()}\n"
            f"Strong: {m['strong']}\n"
            f"Triggers: {', '.join(m['names'])}\n\n"
            f"RSI={row['rsi']:.2f}\n"
            f"%B={row['pctB']:.2f}\n"
            f"K={row['K']:.2f} / D={row['D']:.2f}\n"
            f"CCI={row['cci']:.2f}\n"
            f"MFI={row['mfi']:.2f}"
        )
        sel.annotation.set(text=text, fontsize=9)

    ax.set_title("Multi-Indicator Reversal Detection + Strong Signals ★")
    ax.grid(True)
    plt.show()


# =========================================
# 使用示例
# =========================================
if __name__ == "__main__":
    # df = pd.read_csv(glob.glob("../output/price/2025/qqq/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/iren/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2024/iren/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2023/iren/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2022/iren/part-00000-*-c000.csv")[0])
    df = pd.read_csv(glob.glob("../output/price/2025/2025-11-24/nbis/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/cifr/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/wulf/part-00000-*-c000.csv")[0])

    # df = pd.read_csv(glob.glob("../output/price/2025/oklo/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/be/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/eose/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2024/eose/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/mp/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/sndk/part-00000-*-c000.csv")[0])

    # df = pd.read_csv(glob.glob("../output/price/2025/amd/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/avgo/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2024/avgo/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2023/avgo/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/crdo/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2024/crdo/part-00000-*-c000.csv")[0])

    # df = pd.read_csv(glob.glob("../output/price/2025/nvda/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/tsla/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/aapl/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/meta/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/goog/part-00000-*-c000.csv")[0])

    # df = pd.read_csv(glob.glob("../output/price/2025/rklb/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/asts/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/onds/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2024/onds/part-00000-*-c000.csv")[0])

    # df = pd.read_csv(glob.glob("../output/price/2025/hood/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/pltr/part-00000-*-c000.csv")[0])

    # df = pd.read_csv(glob.glob("../output/price/2025/ibit/part-00000-*-c000.csv")[0])

    signals, df_calc = detect_all_signals(df)
    plot_signals(df_calc, signals)
