# 示例：通过Python发送机器人消息
import requests
import pandas as pd
import time
from fear_and_greed import get
import datetime

def sendMsg(msg):
    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=0c90c9da-8b10-40b1-9818-61d73758e683"
    data = {
        "msgtype": "text",
        "text": {"content": msg}
    }
    requests.post(webhook_url, json=data)


if(datetime.datetime.now().weekday() < 5):
    fg = get()
    print(f"📈 当前指数：{fg.value}")
    print(f"🧭 情绪等级：{fg.description}")  # extreme fear / fear / neutral / greed / extreme greed
    print(f"🕒 更新时间：{fg.last_update}")

    sends = time.strftime('%Y-%m-%d %H:%M', time.localtime())+"\n\n"
    sendMsg(f"{sends}CNN最新GREED: {round(fg.value,2)}\n情绪等级：{fg.description}")


