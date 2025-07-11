import yfinance as yf
from datetime import datetime, timedelta
import time
import datetime


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
    sends = time.strftime('%Y-%m-%d %H:%M', time.localtime()) + "\n\n"
    # sends = ""

    # index
    for symbol in ["SPY","QQQ"]:
        pct = get_daily_change_percent(symbol, apikey)
        print(f"{symbol} 昨日涨跌幅：{pct}%")
        sends += f"{symbol} 昨日涨跌幅：{pct}%\n"
        time.sleep(8)
    sends += "\n"

    # m7
    li1 = dict()
    avg_sum = 0
    for symbol in ["NVDA", "AAPL", "TSLA", "MSFT", "GOOG", "AMZN", "META"]:
        pct = get_daily_change_percent(symbol, apikey)
        li1[symbol] = pct
        print(f"{symbol} 昨日涨跌幅：{pct}%")
        time.sleep(4)
    for key, value in sorted(li1.items(), key=lambda x: x[1]):
        avg_sum += value
        sends += f"{key} 昨日涨跌幅：{value}%\n"
    sends += f"-M7 昨日平均涨跌幅：{round(avg_sum / 7, 2)}%-\n"

    # medium
    li2 = dict()
    for symbol in ["PLTR", "MSTR", "TSM", "AVGO", "NFLX", "SMCI", "HOOD", "COIN", "AMD","MU"]:
        pct = get_daily_change_percent(symbol, apikey)
        li2[symbol] = pct
        print(f"{symbol} 昨日涨跌幅：{pct}%")
        time.sleep(8)
    for key, value in sorted(li2.items(), key=lambda x: x[1]):
        sends += f"\n{key} 昨日涨跌幅：{value}%"
    sends += "\n"

    # small and extra
    li2 = dict()
    for symbol in ["IBIT", "CRCL"]:
        pct = get_daily_change_percent(symbol, apikey)
        li2[symbol] = pct
        print(f"{symbol} 昨日涨跌幅：{pct}%")
        time.sleep(8)
    for key, value in sorted(li2.items(), key=lambda x: x[1]):
        sends += f"\n{key} 昨日涨跌幅：{value}%"
    sendMsg(sends)