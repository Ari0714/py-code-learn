import glob

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ——————————————
# 输入数据 df: 必须包含 close、volume
# ——————————————
# 示例：读取本地 CSV
# df = pd.read_csv("data.csv")
stock_name = "qqq"
end_date = "2025-12-06"
df = pd.read_csv(glob.glob(f"output/rsi_union/2025/{end_date}/{stock_name}/part-00000-*-c000.csv")[0])

# 下载数据
# df = yf.download("AAPL", start="2024-01-01")

# True Range
df["H-L"] = df["high"] - df["low"]
df["H-PC"] = abs(df["high"] - df["close"].shift(1))
df["L-PC"] = abs(df["low"] - df["close"].shift(1))
df["TR"] = df[["H-L", "H-PC", "L-PC"]].max(axis=1)

# ATR 无未来函数
N = 14
df["ATR"] = df["TR"].rolling(N).mean()

# 波动率空洞值
df["VolHole"] = df["TR"] - df["ATR"]

# 买卖信号（无未来重绘）
df["Buy"] = (df["VolHole"] > 0) & (df["VolHole"].shift(1) < 0) & (df["close"] > df["close"].shift(1))
df["Sell"] = (df["VolHole"] < 0) & (df["VolHole"].shift(1) > 0) & (df["close"] < df["close"].shift(1))

# 绘图
plt.figure(figsize=(14, 7))
plt.plot(df["close"], label="Close", linewidth=1)

# 标注信号
plt.scatter(df.index[df["Buy"]], df["close"][df["Buy"]], marker="^", s=120, label="Buy", color="green")
plt.scatter(df.index[df["Sell"]], df["close"][df["Sell"]], marker="v", s=120, label="Sell", color="red")

# 波动率空洞指标画图
plt.twinx()
plt.plot(df["VolHole"], label="VolHole", linestyle="--", alpha=0.6)

plt.title("Volatility Hole Indicator with Buy/Sell Signals — No Repainting")
plt.legend(loc="upper left")
plt.show()


