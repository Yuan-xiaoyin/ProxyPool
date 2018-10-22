'''异常处理
此模块用于处理一些程序中的error'''
class PoolEmptyError(Exception):
    # 重写init方法
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('代理池已枯竭')
