import time
import requests
import pandas as pd
from datetime import datetime, date, timedelta
from utils.util import createFilePath


# 定义获取 bollinger 数据的函数
def get_bollinger(symbol, start_date, end_date):

    # {'name': 'STOCHF - Stochastic Fast', 'fast_k_period': 14, 'fast_d_period': 3, 'fast_dma_type': 'SMA'}
    api_key = "9b0740741cc74bb2ab03dd90b74e8061"  # 替换为你的 API 密钥
    interval = "1day"  # 时间间隔，常见的有 '1min', '5min', '15min', '1day', '1week' 等

    # Twelve Data API 请求URL
    url = f"https://api.twelvedata.com/bbands?symbol={symbol}&interval={interval}&apikey={api_key}"
    params = {
        "start_date": start_date,
        "end_date": end_date
    }
    # 发送 GET 请求
    response = requests.get(url,params)

    # 检查请求是否成功
    if response.status_code == 200:
        data = response.json()
        print(data)
        if "values" in data:
            # 将数据转换为 DataFrame
            bollinger = pd.DataFrame(data["values"])

            # 转换日期格式为 pandas datetime 格式
            bollinger["datetime"] = pd.to_datetime(bollinger["datetime"])
            bollinger["upper_band"] = bollinger["upper_band"].astype(float)
            bollinger["middle_band"] = bollinger["middle_band"].astype(float)
            bollinger["lower_band"] = bollinger["lower_band"].astype(float)

            return bollinger
        else:
            print("没有获取到 bollinger 数据。")
            return None
    else:
        print(f"请求失败，错误代码：{response.status_code}")
        return None


if __name__ == '__main__':

    # start_date = "2023-11-22"
    # end_date = "2024-11-22"
    # 获取今日日期, 计算去年今日
    # end_date = "2025-11-22"
    end_date = date.today()
    start_date  = date(end_date.year - 1, end_date.month, end_date.day)

    for symbol in [
              "voo", "qqq",
              "iren", "nbis", "crwv", "cifr", "wulf",
              "rklb", "asts", "onds",
              "nvda", "goog", "tsla", "aapl", "meta",
              "amd", "tsm", "avgo", "crdo", "sndk",
              "be", "eose", "oklo",
              "hood","pltr","app",
              "ibit"]:
    # for symbol in [
    #         "aapl"]:

        print(f"\n=========={symbol}============")
        bollinger_data = get_bollinger(symbol,start_date,end_date)

        # 如果获取到数据，展示结果
        if bollinger_data is not None:
            print(bollinger_data.tail())  # 打印最后几行数据

        createFilePath(f"output/bollinger/2025/{end_date}/")
        try:
            bollinger_data.to_csv(f"output/bollinger/2025/{end_date}/bollinger-{symbol}.csv")
        except:
            pass

        time.sleep(10)


