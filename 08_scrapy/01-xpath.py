

# import requests
# from lxml import etree
#
# url = 'https://quotes.sina.cn/global/hq/quotes.php?code=VIX&_refluxos=a10'  # 替换成你实际的网址
# headers = {'User-Agent': 'Mozilla/5.0'}
#
# response = requests.get(url, headers=headers)
# print(response)
# html = etree.HTML(response.text)
# print(html)
#
#
# value = html.xpath('//div[@id="HQBox_Point_price"]/text()')
# print(value)  # 输出示例：17.48

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
import time








