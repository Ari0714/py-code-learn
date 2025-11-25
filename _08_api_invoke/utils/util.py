import requests
from pathlib import Path
import os

def sendMsg(msg):
    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=0c90c9da-8b10-40b1-9818-61d73758e683"
    data = {
        "msgtype": "text",
        "text": {"content": msg}
    }
    requests.post(webhook_url, json=data)

def createFilePath(file_path):
    """自动创建目录并保存文件"""
    # 获取目录路径
    directory = os.path.dirname(file_path)

    # 如果目录不存在，则创建（包括多级目录）
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        print(f"已创建目录: {directory}")

