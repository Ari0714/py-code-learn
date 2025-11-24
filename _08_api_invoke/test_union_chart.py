import glob

import pandas as pd
import matplotlib.pyplot as plt


# 假设 `df` 是包含 `date`, `open`, `high`, `low`, `close`, `volume`, `rsi` 数据的 DataFrame

# def plot_price_rsi(df):
#     df["date"] = pd.to_datetime(df["date"])
#
#     # 创建主图和 RSI 图
#     fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), sharex=True)
#
#     # 主图：绘制收盘价
#     ax1.plot(df["date"], df["close"], label="Close Price", lw=1.2, color='blue')
#     ax1.set_title("Price Chart")
#     ax1.set_ylabel("Price")
#     ax1.grid(True)
#
#     # 绘制 RSI 图
#     ax2.plot(df["date"], df["rsi"], label="RSI", lw=1.2, color='purple')
#
#     # 添加水平线，标示超买区（70）和超卖区（30）
#     ax2.axhline(70, color='red', linestyle="--", label="Overbought (70)")
#     ax2.axhline(30, color='green', linestyle="--", label="Oversold (30)")
#
#     ax2.set_title("RSI Chart")
#     ax2.set_ylabel("RSI")
#     ax2.set_ylim(0, 100)
#     ax2.grid(True)
#     ax2.legend(loc='upper left')
#
#     # 调整图表布局
#     plt.tight_layout()
#
#     # 显示图表
#     plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# 示例数据：包括日期、开盘、最高、最低、收盘、交易量以及MACD相关数据

# 将数据转化为 DataFrame
df = pd.read_csv(glob.glob("output/rsi_union/amd/part-00000-*-c000.csv")[0])
df['date'] = pd.to_datetime(df['date'])

# 计算买入/卖出信号
df['buy_signal'] = (df['macd'] > df['macd_signal']) & (df['macd'].shift(1) < df['macd_signal'].shift(1))
df['sell_signal'] = (df['macd'] < df['macd_signal']) & (df['macd'].shift(1) > df['macd_signal'].shift(1))

# 设置图形大小
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), sharex=True)

# 绘制主图（价格）
ax1.plot(df['date'], df['close'], label='Close Price', color='b', linewidth=1.2)
ax1.set_title('Stock Price and MACD', fontsize=14)
ax1.set_ylabel('Price', fontsize=12)
ax1.grid(True)
ax1.legend(loc='upper left')

# 绘制 MACD 图
ax2.plot(df['date'], df['macd'], label='MACD', color='r', linewidth=1.2)
ax2.plot(df['date'], df['macd_signal'], label='MACD Signal', color='g', linewidth=1.2)
ax2.bar(df['date'], df['macd_hist'], label='MACD Histogram', color='gray', alpha=0.3)

# 绘制买入和卖出信号
ax2.scatter(df['date'][df['buy_signal']], df['macd'][df['buy_signal']], marker='^', color='g', label='Buy Signal', s=100)
ax2.scatter(df['date'][df['sell_signal']], df['macd'][df['sell_signal']], marker='v', color='r', label='Sell Signal', s=100)

ax2.set_title('MACD and Signal with Buy/Sell Signals', fontsize=14)
ax2.set_ylabel('MACD', fontsize=12)
ax2.grid(True)
ax2.legend(loc='upper left')

# 自动调整布局
plt.tight_layout()

# 显示图表
plt.show()


# 示例调用
# df = pd.read_csv(glob.glob("output/rsi_union/amd/part-00000-*-c000.csv")[0])
# plot_price_rsi(df)
