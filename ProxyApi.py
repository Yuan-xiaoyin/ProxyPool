from flask import Flask,g
from RedisDb  import RedisClient

__all__=['app']
app=Flask(__name__)
def get_conn():
    # g相当于global,g对象用来保存用户的数据，g对象在一次请求中所有代码的地方，都是可以使用的
    if not hasattr(g,'redis'):
        # hasattr(object,name):用于判断一个对象中是否存在name这一属性
        g.redis=RedisClient()
    return g.redis
# 定义首页
@app.route('/')
def index():
    return '<h2> Welcome to Proxy Pool System<h2>'

#定义随机代理页
@app.route('/random')
def get_proxy():
    conn=get_conn()
    # 调用RedisClient()方法里的random方法，获取随机代理
    return conn.random()
# 定义获取数量的页面
@app.route('/count')
def get_counts():
    conn=get_conn()
    # 调用RedisClient()方法里的count方法,获取代理池的剩余个数
    return str(conn.count())

if __name__=='__main__':
    app.run()
