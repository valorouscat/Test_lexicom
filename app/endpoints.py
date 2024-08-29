from fastapi import APIRouter, HTTPException
import logging

from app.models import Data, Phone
from db import crud


# logger
logger = logging.getLogger(__name__)

router = APIRouter()


# endpoint for checking data
@router.get("/check_data")
async def check_data(phone: str):
    # validation of phone number
    try:
        val_phone = Phone(phone=phone.strip('\"').strip('\''))
    except ValueError:
        logger.error(f"Invalid phone number: {phone}")
        raise HTTPException(status_code=400, detail="Invalid phone number")
    
    # check if phone number exists
    result = await crud.check_data(val_phone.phone)
    if result is None:
        raise HTTPException(status_code=404, detail="Phone number not found")
    return result


# endpoint for writing data
@router.post("/write_data", response_model=Data)
async def write_data(data: Data):
    # write data
    result = await crud.write_data(data)
    if result is None:
        raise HTTPException(status_code=400, detail="Failed to write data")
    return result


# endpoint for updating data
@router.put('/update_data', response_model=Data)
async def update_data(data: Data):
    result = await crud.update_data(data)
    if result is None:
        raise HTTPException(status_code=400, detail="Failed to update data")
    return result
