import requests

class Util:
    def sendMsg(msg):
        webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=0c90c9da-8b10-40b1-9818-61d73758e683"
        data = {
            "msgtype": "text",
            "text": {"content": msg}
        }
        requests.post(webhook_url, json=data)
