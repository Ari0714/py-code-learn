import time
import requests
import pandas as pd
from datetime import datetime, date, timedelta
from utils.util import createFilePath


# 定义获取 MACD 数据的函数
def get_macd(symbol, start_date, end_date):

    api_key = "9b0740741cc74bb2ab03dd90b74e8061"  # 替换为你的 API 密钥
    interval = "1day"  # 时间间隔，常见的有 '1min', '5min', '15min', '1day', '1week' 等

    # Twelve Data API 请求URL
    url = f"https://api.twelvedata.com/macd?symbol={symbol}&interval={interval}&apikey={api_key}"
    params = {
        "start_date": start_date,
        "end_date": end_date
    }
    # 发送 GET 请求
    response = requests.get(url,params)

    # 检查请求是否成功
    if response.status_code == 200:
        data = response.json()
        if "values" in data:
            # 将数据转换为 DataFrame
            macd_data = pd.DataFrame(data["values"])

            # 转换日期格式为 pandas datetime 格式
            macd_data["datetime"] = pd.to_datetime(macd_data["datetime"])
            macd_data["macd"] = macd_data["macd"].astype(float)
            macd_data["macd_signal"] = macd_data["macd_signal"].astype(float)
            macd_data["macd_hist"] = macd_data["macd_hist"].astype(float)

            return macd_data
        else:
            print("没有获取到 MACD 数据。")
            return None
    else:
        print(f"请求失败，错误代码：{response.status_code}")
        return None


if __name__ == '__main__':

    start_date = "2023-11-22"
    end_date = "2024-11-22"
    # 获取今日日期, 计算去年今日
    # end_date = "2025-11-22"
    # end_date = date.today()
    # start_date  = date(end_date.year - 1, end_date.month, end_date.day)

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
        macd_data = get_macd(symbol,start_date,end_date)

        # 如果获取到数据，展示结果
        if macd_data is not None:
            print(macd_data.tail())  # 打印最后几行数据

        createFilePath(f"output/macd/2024/{end_date}/")
        try:
            macd_data.to_csv(f"output/macd/2024/{end_date}/macd-{symbol}.csv")
        except:
            pass

        time.sleep(10)


