'''获取网页模块
用requests模块来获取要爬取的每个网页的html'''
import time

import requests
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq
def get_page(url):
    headers={'UserAgent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

    try:
        response=requests.get(url=url,headers=headers)
        if response.status_code==200:
            print('抓取成功:',url)
            return response.text
    except ConnectionError:
        print('抓取失败:',url)
        return None

