'''将抓取的数据存入到数据库中'''
from RedisDb import RedisClient
from Crawler import Crawler
from settings import *
import sys

class Getter():
    def __init__(self):
        # 对这两个方法进行初始化
        self.redis=RedisClient()
        self.crawler=Crawler()
    def is_over_threshold(self):
        '''判断代理池的数量书否达到设置的值,达到数量了就返回True，否则返回False'''
        if self.redis.count()>=POOL_UPPER_HRESHOLD:
            return True
        return False
    def run(self):
        print('获取器开始执行...')
        # 如果没有达到数量
        if not self.is_over_threshold():
            # 遍历__CrawlFuncCount__：比如说，当__CrawlFuncCount__==0的时候，callback就取得数crawlFunc里面的索引为0的方法
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                # 获取所有以crawl_开头方法的列表
                callback=self.crawler.__CrawlFunc__[callback_label]
                # 调用get_proxies方法，获取抓取到的代理
                proxies=self.crawler.get_proxies(callback)
                sys.stdout.flush()
                # 遍历获取到的代理，添加到数据库中
                for proxy in proxies:
                    self.redis.add(proxy)





