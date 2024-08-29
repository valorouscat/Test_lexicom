from fastapi import FastAPI
from contextlib import asynccontextmanager
import aioredis
import json
import logging 

from app.models import Data, Phone


logger = logging.getLogger(__name__)

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
    logger.info("Connected to Redis")
    yield
    await redis.close()
    logger.info("Redis connection closed")


async def check_data(phone: Phone):
    logger.info(f"Checking phone number {phone}")
    data = await redis.get(f'phone:{phone}')

    if data: 
        try: 
            address = json.loads(data).get('address')
            if address:
                return address
            
            else:
                logger.warning(f"Address for {phone} not found")
                return 'None'

        except json.JSONDecodeError:
            logger.exception("Invalid JSON data in database")
        
    else:
        logger.error(f"Phone number {phone} not found")
        return None


async def write_data(data: Data):
    existing_data = await redis.exists(f'phone:{data.phone}')

    if not existing_data:
        logger.info(f"Writing new data for {data.phone}")
        try: 
            result = await redis.set(f'phone:{data.phone}', data.model_dump_json())
            if result:
                return data

            else:
                logger.error(f"Failed to write data for {data.phone}")
                return None
            
        except Exception:
            logger.exception(f"Failed to write data for {data.phone}")
            return None
        
    else:
        logger.info(f"Phone number {data.phone} already exists")
        return None


async def update_data(data: Data):
    existing_data = await redis.exists(f'phone:{data.phone}')

    if existing_data:
        logger.info(f"Updating data for {data.phone}")
        try:
            result = await redis.set(f'phone:{data.phone}', data.model_dump_json())
            if result:
                return data
            
            else:
                logger.error(f"Failed to update data for {data.phone}")
                return None
            
        except Exception:
            logger.exception(f"Failed to update data for {data.phone}")
    
    else:
        logger.info(f"Phone number {data.phone} not found")
        return None
