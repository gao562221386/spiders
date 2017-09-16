import redis
from pymongo import MongoClient
import json

# 了连接redis
redis_cli = redis.Redis(host='10.254.8.100', port=6379, db=0)

# 连接mongodb
handle = MongoClient('127.0.0.1', 27017)
db = handle['Tianqi']
col = db['tianqi']

# 循环读写操作
while True:
    # 从redis中使用key获取数据, 返回能够获取数据的key及对应的数据
    sourse, data = redis_cli.blpop(['tianqi:items'])
    # print(type(data.decode))

    # 将数据转换成Python字典
    result = json.loads(data.decode())
    print(result)
    col.insert(result)