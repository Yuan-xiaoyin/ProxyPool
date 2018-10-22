'''设置模块
用来保存每个模块的基础设置'''


# RedisDb要用到的配置文件
MAX_SCORE=100
MIN_SCORE=0
INITIAL_SCORE=10
REDIS_HOST='localhost'
REDIS_PORT=6379
REDIS_PASSWORD=None
REDIS_KEY='proxies'

# getter获取器要用到的相关配置
# 用来设置代理池代理的数量
POOL_UPPER_HRESHOLD=1000


# 测试模块要用到的相关配置
# 这是测试的目标网站，这里原则的是这种响应比较稳定的，就选的百度
TEST_URL='https://www.baidu.com'
# 响应状态码，如果为200，就表示正常响应，也可以加其他的状态码进去做一些响应的处理，这里不需要就添加一个就好了
TEST_STATUS_CODE=[200]
# 每次测试的最大个数
TEST_SIZE=100


# Scheduler模块要用到的相关配置
TESTER_CYCLE=20
GETTER_CYCLE=300
# 定义三个常量分表表示测试模块，获取模块，接口模块的开关，如果为true表示开启
TESTER_ENABLED=True
GETTER_ENABLED=True
API_ENABLED=True

API_HOST='127.0.0.1'
API_PORT=5000




