import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

# ----------------------------------------
# 计算 Bollinger Band 与 %B（只用历史数据）
# ----------------------------------------
def compute_bollinger_pctb(df, n=20, k=2):
    """
    输入 df 必须包含: 'date', 'close'
    返回 df 拷贝，包含列: ma, std, upper, lower, pctb
    注意：rolling 默认是 past-only（不含未来），安全。
    """
    df = df.copy().reset_index(drop=True)
    df['ma'] = df['close'].rolling(window=n, min_periods=1).mean()  # past n
    df['std'] = df['close'].rolling(window=n, min_periods=1).std(ddof=0)  # sample/std
    df['upper'] = df['ma'] + k * df['std']
    df['lower'] = df['ma'] - k * df['std']
    # 防止除以零
    df['pctB'] = (df['close'] - df['lower']) / (df['upper'] - df['lower'] + 1e-12)
    return df

# ----------------------------------------
# 无未来的 %B 反转检测规则（只用 i-1 和 i）
# ----------------------------------------
def detect_pctb_reversal_no_lookahead(df, up_thresh=0.95, down_thresh=0.05):
    """
    规则（无未来）：
      - 顶部信号（sell）:
          pctB[i-1] > 1.0  且 pctB[i] < up_thresh   （从上轨回落）
      - 底部信号（buy）:
          pctB[i-1] < 0.0  且 pctB[i] > down_thresh (从下轨回升)
    参数 up_thresh/down_thresh 可调（默认 0.95 / 0.05）
    返回: DataFrame signals，含 index,date,close,pctB,signal ('buy'/'sell')
    """
    df = df.copy().reset_index(drop=True)
    pct = df['pctB'].values
    inds = []
    signals = []

    # 从 i=1 开始，因为要比较 i-1 与 i（无未来）
    for i in range(1, len(df)):
        prev = pct[i-1]
        cur = pct[i]

        # 顶部：昨天 >1，今天回落到 < up_thresh
        if (prev > 1.0) and (cur < up_thresh):
            inds.append(i)
            signals.append('sell')
            continue

        # 底部：昨天 <0，今天回升到 > down_thresh
        if (prev < 0.0) and (cur > down_thresh):
            inds.append(i)
            signals.append('buy')

    if len(inds) == 0:
        return pd.DataFrame(columns=['index','date','close','pctB','signal'])

    out = pd.DataFrame({
        'index': inds,
        'date': df.loc[inds, 'date'].values,
        'close': df.loc[inds, 'close'].values,
        'pctB': df.loc[inds, 'pctB'].values,
        'signal': signals
    })
    out = out.reset_index(drop=True)
    return out

# ----------------------------------------
# 简单绘图（价格+BB + %B + 信号）
# ----------------------------------------
def plot_pctb_with_signals(df, signals_df=None):
    """
    df: output of compute_bollinger_pctb (含 date, close, upper, ma, lower, pctB)
    signals_df: detect_pctb_reversal_no_lookahead 返回表（可 None）
    """
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])

    fig, (ax1, ax2) = plt.subplots(2,1, figsize=(14,8), sharex=True,
                                   gridspec_kw={'height_ratios':[2,1]})
    # price + bands
    ax1.plot(df['date'], df['close'], label='close', linewidth=1.2)
    ax1.plot(df['date'], df['upper'], linestyle='--', label='upper')
    ax1.plot(df['date'], df['ma'], linestyle='-', label='ma')
    ax1.plot(df['date'], df['lower'], linestyle='--', label='lower')

    if signals_df is not None and not signals_df.empty:
        buys = signals_df[signals_df['signal']=='buy']
        sells = signals_df[signals_df['signal']=='sell']
        if not buys.empty:
            ax1.scatter(pd.to_datetime(buys['date']), buys['close'], marker='^', color='green', s=100, label='buy')
        if not sells.empty:
            ax1.scatter(pd.to_datetime(sells['date']), sells['close'], marker='v', color='red', s=100, label='sell')

    ax1.legend(loc='upper left')
    ax1.set_title('Price + Bollinger Bands')

    # pctB subplot
    ax2.plot(df['date'], df['pctB'], label='%B', linewidth=1.0)
    ax2.axhline(1.0, color='gray', linestyle='--')
    ax2.axhline(0.0, color='gray', linestyle='--')
    ax2.axhline(0.05, color='green', linestyle='--', linewidth=0.8)
    ax2.axhline(0.95, color='red', linestyle='--', linewidth=0.8)

    if signals_df is not None and not signals_df.empty:
        if not buys.empty:
            ax2.scatter(pd.to_datetime(buys['date']), buys['pctB'], color='green', s=60)
        if not sells.empty:
            ax2.scatter(pd.to_datetime(sells['date']), sells['pctB'], color='red', s=60)

    ax2.set_title('%B and thresholds')
    plt.tight_layout()
    plt.show()

# ----------------------------------------
# 使用示例（本地运行）
# ----------------------------------------
if __name__ == "__main__":

    # df = pd.read_csv(glob.glob("../output/price/2025/qqq/part-00000-*-c000.csv")[0])
    df = pd.read_csv(glob.glob("../output/price/2025/2025-11-24/iren/part-00000-*-c000.csv")[0])
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

    df_bb = compute_bollinger_pctb(df, n=20, k=2)
    signals = detect_pctb_reversal_no_lookahead(df_bb, up_thresh=0.95, down_thresh=0.05)

    print("Detected signals:")
    print(signals)

    plot_pctb_with_signals(df_bb, signals)
