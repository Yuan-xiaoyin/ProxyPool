'''存储模块
将得到的代理放到redis数据库中'''

import redis

from PoolError import PoolEmptyError
from settings import *
from random import choice


class RedisClient(object):
    # 对redis数据库的连接初始化
    def __init__(self,host=REDIS_HOST,password=REDIS_PASSWORD,port=REDIS_PORT):
        self.db=redis.StrictRedis(host=host,port=port,password=password,decode_responses=True)
    # 添加代理，并且设置新代理分数的初始值为10
    def add(self,proxy,score=INITIAL_SCORE):
        # self.db.zscore()返回关键字的score值，如果没有，则将REDIS_KEY的代理分数添加
        if not self.db.zscore(REDIS_KEY,proxy):
            return self.db.zadd(REDIS_KEY,score,proxy)

    def random(self):
#         此函数表示随机返回分数最高的代理，如果最高分数不存在，则按照排名获取

        # 返回键名为REDIS_KEY的有序集合中，分数为MAX_SCORE（最高分)之间的元素,返回值为列表
        result=self.db.zrangebyscore(REDIS_KEY,MAX_SCORE,MAX_SCORE)
        if len(result):
            # 随机返回分数最高的其中一个（因为我们的MAX_SCORE=100)
            return choice(result)
        else:
            # 返回键名为REDIS_KEY的有序集合中，分数为MAX_SCORE（最高分)之间的元素,返回值为列表
            result=self.db.zrevrange(REDIS_KEY,MIN_SCORE,MAX_SCORE)
            if len(result):
                # zrevrange返回的是一个由大到小排列有序集合，因为分数可以重复，所以随机返回一个其中分数最高的元素
                return choice(result)
            else:
                # 否则就抛出异常
                raise PoolEmptyError
    def decrease(self,proxy):
        # 此函数是在代理检测无效的时候设置分数减1的方法，如果代理的分数达到最低值则删除代理
        # score表示返回检测后代理的分数
        score=self.db.zscore(REDIS_KEY,proxy)
        # 如果有返回的score并且socre的分数大于最低分数
        if score and score>MIN_SCORE:
            print('代理',proxy,'当前分数',score,'减1')
            # zincrby（）方法表示在键名为REDIS_KEY的有序集合中，如果存在proxy,则在proxy的基础上减1，否则向集合中添加该元素，初始值为-1
            return self.db.zincrby(REDIS_KEY,proxy,-1)
        else:
            print('代理',proxy,'当前分数',score,'删除')
            # zrem（）方法表示删除键名为REDIS_KEY集合中的proxy元素
            return self.db.zrem(REDIS_KEY,proxy)

    def exists(self,proxy):
        '''此函数表示判断proxy元素是否存在于集合为REDIS_KEY的集合中'''

        # 如果返回None,则表示不存在与集合中，如果不是None则表示存在集合中
        return not self.db.zscore(REDIS_KEY,proxy)==None
    def max(self,proxy):
        '''此函数示意将有效代理的分数设置MAX_SCORE'''
        print('代理',proxy,'可用，设置为',MAX_SCORE)
        # 向集合中添加元素MAX_SCORE,proxy(将proxy的值设置为MAX_SOCRE)
        return self.db.zadd(REDIS_KEY,MAX_SCORE,proxy)

    def count(self):
        '''返回当前集合的元素个数'''
        # redis.zcard（）方法：返回键名为REDIS_KEY的集合元素的个数
        return self.db.zcard(REDIS_KEY)
    def all(self):
        '''返回所有代理列表，以供检测使用'''
        # redis.zrangebyscore（）方法返回在区间为min_score，max_score之间的所有元素的列表
        return self.db.zrangebyscore(REDIS_KEY,MIN_SCORE,MAX_SCORE)
    def batch(self,start,stop):
        return self.db.zrevrange(REDIS_KEY,start,stop-1)


if __name__=='__main__':
    conn=RedisClient()
    result=conn.batch(2,18)
    print(result)





