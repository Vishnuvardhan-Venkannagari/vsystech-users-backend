import redis


class RedisModel:

    def __init__(self):
        self.rclient = redis.Redis(host='localhost', port=6379, decode_responses=True)

    def get(self, key):
        return self.rclient.get(key)

    def post(self, key, input):
        return self.rclient.set(key, input)

    def delete(self, key):
        return self.rclient.delete(key)
    
    def hset(self, key, input, expiry_seconds):
        return self.rclient.setex(key, expiry_seconds, input)