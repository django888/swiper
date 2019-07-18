broker_url = 'redis://127.0.0.1:6379/0'
broker_pool_limit = 200  # Borker 连接池, 默认是10

timezone = 'Asia/Shanghai'#注明是北京时间,不然就是UTC时间,所以必须设置
accept_content = ['pickle', 'json']

task_serializer = 'pickle'#pickle是序列化的工具

result_backend = 'redis://127.0.0.1:6379/0'
result_serializer = 'pickle'
result_cache_max = 10000  # 任务结果最大缓存数量
result_expires = 3600  # 任务过期时间

worker_redirect_stdouts_level = 'INFO'
