# 示例：通过Python发送机器人消息
import requests
import pandas as pd
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
import time


def sendMsg(msg):
    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=0c90c9da-8b10-40b1-9818-61d73758e683"
    data = {
        "msgtype": "text",
        "text": {"content": msg}
    }
    requests.post(webhook_url, json=data)


def get_vix_cboe_csv():
    try:
        # 设置无头模式（可选）
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

        # 🧩 最关键的参数 ↓↓↓
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--remote-debugging-port=9222")

        # 启动浏览器
        driver = webdriver.Chrome(options=options)

        # 打开页面
        driver.get('https://quotes.sina.cn/global/hq/quotes.php?code=VIX&_refluxos=a10')  # 替换成你的实际网址
        time.sleep(15)  # 等待页面渲染完成（或使用 WebDriverWait 更稳）

        # 获取渲染后的页面 HTML
        html = driver.page_source

        # 用 lxml 解析
        tree = etree.HTML(html)
        value = tree.xpath('//div[@id="hqbox_detail_price"]/text()')[0]
        value_change = tree.xpath('//span[@id="hqbox_detail_change"]/text()')[0]
        value_percent = tree.xpath('//span[@id="hqbox_detail_percent"]/text()')[0]
        driver.quit()

        return value + ', ' + value_change + ', ' + value_percent  # 获取最新收盘价
    except Exception as e:
        print(f"CBOE CSV获取失败: {e}")
        return None


if __name__ == '__main__':
    print("VIX: " + str(get_vix_cboe_csv()))

    sends = time.strftime('%Y-%m-%d %H:%M', time.localtime()) + "\n\n"
    sendMsg(f"{sends}VIX: {str(get_vix_cboe_csv())}")
