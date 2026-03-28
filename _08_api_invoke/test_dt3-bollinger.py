import glob

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter


def detect_rsi_slope_signals(df, rsi_col='rsi', high=70, low=30):
    df = df.copy()
    df = df.reset_index(drop=True)

    # 计算 RSI 斜率
    df['rsi_slope'] = df[rsi_col].diff()

    # 斜率方向转换（仅用当前与上一根，不看未来 → 无重绘）
    df['slope_turn_down'] = (df['rsi_slope'] < 0) & (df['rsi_slope'].shift(1) > 0)  # 正 → 负
    df['slope_turn_up']   = (df['rsi_slope'] > 0) & (df['rsi_slope'].shift(1) < 0)  # 负 → 正

    # 顶部卖出信号
    df['sell_signal'] = df['slope_turn_down'] & (df[rsi_col] > high)

    # 底部买入信号
    df['buy_signal'] = df['slope_turn_up'] & (df[rsi_col] < low)

    # 信号字段：1=买  -1=卖  0=无
    df['signal'] = np.where(df['buy_signal'], 1,
                      np.where(df['sell_signal'], -1, 0))

    return df

def plot_rsi_slope(df, out_png='rsi_slope_signal.png'):
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    else:
        df['date'] = pd.date_range(start='2000-01-01', periods=len(df))

    fig, (ax_p, ax_rsi) = plt.subplots(2, 1, figsize=(14, 9), sharex=True,
                                       gridspec_kw={'height_ratios': [3, 1]})

    # 价格图
    ax_p.plot(df['date'], df['close'], label='Close', linewidth=1)

    buys = df[df['signal'] == 1]
    sells = df[df['signal'] == -1]
    if not buys.empty:
        ax_p.scatter(buys['date'], buys['close'], marker='^', s=130,
                     label='RSI Slope Buy', zorder=5)
    if not sells.empty:
        ax_p.scatter(sells['date'], sells['close'], marker='v', s=130,
                     label='RSI Slope Sell', zorder=5)

    ax_p.legend(loc='upper left')
    ax_p.grid(True, linestyle=':')

    # RSI 图
    ax_rsi.plot(df['date'], df['rsi'], label='RSI', linewidth=1)
    ax_rsi.axhline(70, color='gray', linestyle='--', linewidth=1)
    ax_rsi.axhline(30, color='gray', linestyle='--', linewidth=1)
    ax_rsi.set_ylabel("RSI")
    ax_rsi.grid(True, linestyle=':')

    # 时间格式
    ax_p.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()

    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    plt.show()
    print(f"Chart saved → {out_png}")


if __name__ == '__main__':
    stock_name = "iren"
    end_date = "2025-12-06"
    df = pd.read_csv(glob.glob(f"output/rsi_union/2025/{end_date}/{stock_name}/part-00000-*-c000.csv")[0])

    df = detect_rsi_slope_signals(df)
    df.to_csv("rsi_slope_signals_output.csv", index=False)
    print(df[['date', 'close', 'rsi', 'rsi_slope', 'signal']].tail(10))
    plot_rsi_slope(df)