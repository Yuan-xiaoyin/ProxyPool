'''获取代理的类'''
import json
from pyquery import PyQuery as pq
from GetPage import get_page
import time

class ProxyMetaclass(type):
    '''定义一个元类，用来获取所有以crawl_开头的方法'''

    def __new__(cls,name,bases,attrs):
        # 重写__new__方法
        count=0
        # 定义一个CrawlFunc属性，返回的是一个包含crawl_开头的方法的列表
        attrs['__CrawlFunc__']=[]
        for k,v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count+=1
        attrs['__CrawlFuncCount__']=count
        # 返回一个类的对象
        return type.__new__(cls,name,bases,attrs)
class Crawler(object,metaclass=ProxyMetaclass):
    # 得到代理，其中的callback是后面在调度器的时候定义的一个回调函数
    def get_proxies(self,callback):
        # 定义一个空列表，最后返回这个列表
        proxies=[]
        # ecal():将字符串变为有效的表达式参与运算并返回结果，这里相当于是遍历self.callback()
        for proxy in eval('self.{}()'.format(callback)):
            print('成功获取代理:',proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self,page_count=4):
        # 开始的url
        start_url='http://www.66ip.cn/{}.html'
        # 对每页的url进行拼接
        urls=[start_url.format(page) for page in range(1,page_count+1)]
        for url in urls:
            time.sleep(1)
            print('正在爬取:',url)
            html=get_page(url)
            if html:
                # 解析html，这里用的pyquery这个库来进行解析
                doc=pq(html)
                trs=doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    # nth-child 属于伪类选择器，表示第几个子节点
                    ip=tr.find('td:nth-child(1)').text()
                    port=tr.find('td:nth-child(2)').text()
                    # 生成的额ip与port是字符串的形式，这里可以用join来进行拼接得到ip:port
                    yield ":".join([ip,port])
        # 也可以用xpath来解析得到
        # html=etree.HTML(html)
        # ip=html.xpath('//div[@align="center"]/table/tr/td[1]/text()')
        # port=html.xpath('//div[@align="center"]/table/tr/td[2]/text()')
        # 得到的Ip与port是列表的形式，所以用zip函数来进行拼接
        # # results=zip(ip,port)
        # # for i in results:
        # #     result=":".join(i)
        # #     print([result])
    def crawl_swei360(self,page_count=10):
        '''获取代理360上面的免费代理'''
        start_url='http://www.swei360.com/?page={}'
        urls=[start_url.format(page) for page in range(1,page_count+1)]
        for url in urls:
            time.sleep(1)
            print('正在抓取:',url)
            html=get_page(url)
            if html:
                doc=pq(html)
                trs=doc('#list table tbody tr').items()
                for tr in trs:
                    ip=tr.find('td:nth-child(1)').text()
                    port=tr.find('td:nth-child(2)').text()
                    yield ":".join([ip,port])
    def crawl_Kuaidaili(self,page_count=5):
        '''获取快代理网站的免费代理'''
        start_url='https://www.kuaidaili.com/free/inha/{}/'
        urls=[start_url.format(page) for page in range(1,page_count+1)]
        for url in urls:
            print('正在抓取快代理:',url)
            # 这里要加一个睡眠时间，太快容易报503错误
            time.sleep(1)
            html=get_page(url)
            if html:
                doc=pq(html)
                trs=doc('#list table tbody tr').items()
                for tr in trs:
                    ip=tr.find('td:nth-child(1)').text()
                    port=tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip,port])








