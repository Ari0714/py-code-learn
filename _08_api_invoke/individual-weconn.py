import yfinance as yf
from datetime import datetime, timedelta
import time
import datetime

# def get_stock_change(symbols=["AAPL", "TSLA"]):
#     end_date = datetime.now()
#     start_date = end_date - timedelta(days=7)  # 获取近7天数据确保覆盖交易日
#
#     try:
#         data = yf.download(symbols, start=start_date, end=end_date, progress=False)
#         changes = {}
#         for symbol in symbols:
#             close_prices = data['Close'][symbol]
#             if len(close_prices) >= 2:
#                 last_close = close_prices.iloc[-1]
#                 prev_close = close_prices.iloc[-2]
#                 changes[symbol] = (last_close - prev_close) / prev_close * 100
#         return changes
#     except Exception as e:
#         print(f"获取数据失败: {e}")
#         return None
#
# # 测试
# changes = get_stock_change()
# print(f"昨日涨跌幅: {changes}")

import requests

def sendMsg(msg):
    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=0c90c9da-8b10-40b1-9818-61d73758e683"
    data = {
        "msgtype": "text",
        "text": {"content": msg}
    }
    requests.post(webhook_url, json=data)


def get_daily_change_percent(symbol, apikey):
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&outputsize=2&apikey={apikey}"
    resp = requests.get(url).json()
    try:
        # print(resp['values'])
        latest = float(resp['values'][0]['close'])
        prev = float(resp['values'][1]['close'])
        change_pct = ((latest - prev) / prev) * 100
        return round(change_pct, 2)
    except Exception as e:
        print(f"⚠️ 解析失败: {e}")
        return None

# 示例调用
if(datetime.datetime.now().weekday() < 5):
    apikey = "9b0740741cc74bb2ab03dd90b74e8061"  # 替换为你的 Twelve Data Key
    avg_sum = 0
    sends = time.strftime('%Y-%m-%d %H:%M', time.localtime())+"\n\n"
    index = 0
    for symbol in ["NVDA", "AAPL", "TSLA", "MSFT", "GOOG", "AMZN", "META","QQQ"]:
        pct = get_daily_change_percent(symbol, apikey)
        if("QQQ" != symbol):
            avg_sum += pct
            print(f"{symbol} 昨日涨跌幅：{pct}%")
            sends += f"{symbol} 昨日涨跌幅：{pct}%\n"
        if ("QQQ" == symbol):
            index = pct
    print(f"\nM7 昨日平均涨跌幅：{round(avg_sum/7,2)}%")
    print(f"QQQ 昨日涨跌幅 {index}%")
    sendMsg(sends+f"\nM7 昨日平均涨跌幅：{round(avg_sum/7,2)}% \nQQQ 昨日涨跌幅：{index}%")
