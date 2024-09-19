# import redis
# import aioredis

# async def get_redis_connection() -> aioredis.Redis:
#     '''
#     Create a redis connection
#     '''
#     return await aioredis.from_url("redis://localhost:6379", encoding='utf8')
import redis.asyncio as redis

async def get_redis_connection() -> redis.Redis:
    '''
    Create a redis connection using the async redis-py
    '''
    return await redis.from_url("redis://localhost:6379", encoding='utf-8')
