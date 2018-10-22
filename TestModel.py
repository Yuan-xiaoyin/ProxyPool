import asyncio
import sys
import time

from settings import *
import aiohttp
from RedisDb import RedisClient
class Tester(object):
    def __init__(self):
        self.redis=RedisClient()

    async def test_single_proxy(self,proxy):
        '''测试单个代理'''
        conn=aiohttp.TCPConnector(verify_ssl=False)
        # 异步的创建会话
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                # 判断返回对象的类型
                if isinstance(proxy,bytes):
                    # 转码为utf-8类型
                    proxy=proxy.decode('utf-8')
                # 构造代理连接
                real_proxy='http://'+proxy
                print('正在测试:',proxy)
                # 构造异步请求
                async with session.get(TEST_URL,proxy=real_proxy,timeout=15,allow_redirects=False) as response:
                    # 如果成功的返回响应，就将proxy设置为100
                    if response.status in TEST_STATUS_CODE:
                        self.redis.max(proxy)
                        print('代理可用:',proxy)
                    else:
                        # 如果不能响应就在原来的基础之上减一
                        self.redis.decrease(proxy)
                        print('响应码不合法：',proxy,response.status)
            except (aiohttp.ClientError, aiohttp.ClientConnectorError, asyncio.TimeoutError, AttributeError) as e:
                print(e)
                self.redis.decrease(proxy)
                print('代理请求失败',proxy)

    def run(self):
        '''测试主函数，获取所有的代理列表，使用aiohttp分配任务，启动运行，然后进行异步检测'''
        print('测试器开始运行')
        try:
            count=self.redis.count()
            print('当前剩余代理个数：',count)
            for i in range(0,count,TEST_SIZE):
                start=i
                stop=min(i+TEST_SIZE,count)
                print('正在测试第:',start+1,'-',stop,'个代理')
                test_proxies=self.redis.batch(start,stop)


                # 创建循环事件，进行批量测试
                loop=asyncio.get_event_loop()
            # # 遍历列表，以test_size的方式切片进行批量测试
            # for i in range(0,len(proxies),TEST_SIZE):
            #     test_proxies=proxies[i:i + TEST_SIZE]
            # #     然后进行单个 测试
                task=[self.test_single_proxy(proxy) for proxy in test_proxies]
                # run_until_complete运行程序,asyncio.wait获取协同程序的列表，同时返回一个将他们包含在内的协同程序
                loop.run_until_complete(asyncio.wait(task))
                # 刷新页面
                sys.stdout.flush()
                time.sleep(5)
        except Exception as e:
            print('测试器发生错误：',e)





