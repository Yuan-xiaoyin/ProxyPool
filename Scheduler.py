import time
from multiprocessing import Process
from ProxyApi import app
from getter import Getter
from TestModel import Tester
from settings import *

class Scheduler():
    def scheduler_tester(self,cycle=TESTER_CYCLE):
        # 调度测试模块
        '''定时测试代理'''
        tester=Tester()
        while True:
            print('测试器开始运行')
            tester.run()
            time.sleep(cycle)
    def scheduler_getter(self,cycle=GETTER_CYCLE):
        # 调度获取模块
        '''定时获取代理'''
        getter=Getter()
        while True:
            print('开始抓取代理')
            getter.run()
            time.sleep(cycle)
    def scheduler_api(self):
        # 调用接口模块
        '''开启api接口'''
        app.run(API_HOST,API_PORT)

    def run(self):
        '''程序的启动入口'''
        # 分别判断三个模块的开关，如果开启，启动时就新建一个process进程，然后运行，三个进程并行执行，互不影响
        print('代理池开始运行')
        if TESTER_ENABLED:
            tester_process=Process(target=self.scheduler_tester)
            tester_process.start()
        if GETTER_ENABLED:
            getter_process=Process(target=self.scheduler_getter)
            getter_process.start()
        if API_ENABLED:
            api_process=Process(target=self.scheduler_api)
            api_process.start()