# 示例：通过Python发送机器人消息
import requests
import pandas as pd
import time
import datetime

def sendMsg(msg):
    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=0c90c9da-8b10-40b1-9818-61d73758e683"
    data = {
        "msgtype": "text",
        "text": {"content": msg}
    }
    requests.post(webhook_url, json=data)


def get_vix_cboe_csv():
    url = "https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv"
    try:
        df = pd.read_csv(url)
        return df.iloc[-1]["CLOSE"]  # 获取最新收盘价
    except Exception as e:
        print(f"CBOE CSV获取失败: {e}")
        return None

if(datetime.datetime.now().weekday() < 5):
    print("CBOE最新VIXk: " + str(get_vix_cboe_csv()))

    sends = time.strftime('%Y-%m-%d %H:%M', time.localtime())+"\n\n"
    sendMsg(f"{sends}CBOE最新VIX: {str(get_vix_cboe_csv())}")


