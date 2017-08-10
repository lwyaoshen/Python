from redis import StrictRedis
redis = StrictRedis()

redis.set('name','yangsheng')
print(redis.get('name').decode())
