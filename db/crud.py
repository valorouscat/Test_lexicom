from fastapi import FastAPI
from contextlib import asynccontextmanager
import aioredis
import json
import logging 


logger = logging.getLogger(__name__)
#TODO добавить логи для функций

# global variable to hold connection
redis = None

async def redis_pool():
    # Redis client bound to pool of connections (auto-reconnecting).
    return aioredis.from_url(
        "redis://redis:6379", encoding="utf-8", decode_responses=True
    )

# lifespan function
@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis
    redis = await redis_pool()
    print("Connected to Redis")
    yield
    await redis.close()
    print("Redis connection closed")


async def check_data(phone):
    data = await redis.get(f'phone:{phone}')
    if data: 
        return json.loads(data)
        #XXX должен возвращаться только адрес 


async def write_data(data):
    existing_data = await redis.get(f'phone:{data.phone}')
    if existing_data:
        return None
    result = await redis.set(f'phone:{data.phone}', data.json())
    if result:
        return data
    #TODO возвращать только код ответа

async def update_data(data):
    existing_data = await redis.get(f'phone:{data.phone}')
    if existing_data:
        await redis.set(f'phone:{data.phone}', data.json())
        return data
    #TODO возвращать только код ответа
