import redis
import aioredis

async def get_redis_connection() -> aioredis.Redis:
    '''
    Create a redis connection
    '''
    return await aioredis.from_url("redis://localhost:6379", encoding='utf8')