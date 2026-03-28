import requests
import pandas as pd
import matplotlib.pyplot as plt



api_key = '9b0740741cc74bb2ab03dd90b74e8061'

symbol = "COIN"  # ETF，替代性参考标的
interval = "1day"
outputsize = 200

url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&outputsize={outputsize}&apikey={api_key}"

response = requests.get(url)
data = response.json()

# 将数据转为 DataFrame
df = pd.DataFrame(data["values"])
df["datetime"] = pd.to_datetime(df["datetime"])
df["volume"] = df["volume"].astype(float)

df = df.sort_values("datetime")

# 简单画出成交量
plt.figure(figsize=(12, 5))
plt.plot(df["datetime"], df["volume"], label="SPY Volume")
plt.title("SPY Volume - Twelve Data")
plt.xlabel("Date")
plt.ylabel("Volume")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
