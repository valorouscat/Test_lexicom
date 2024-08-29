from fastapi import APIRouter, HTTPException
import logging

from app.models import Data, Phone
from db import crud

# logger
logger = logging.getLogger(__name__)
#TODO добавить логи для всех ручек

router = APIRouter()


@router.get("/check_data")
async def check_data(phone: str):
    # validation of phone number
    try:
        val_phone = Phone(phone=phone)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid phone number")
    
    result = await crud.check_data(val_phone.phone)
    if result is None:
        raise HTTPException(status_code=404, detail="Phone number not found")
    return result


# endpoint for writing and updating data
@router.post("/write_data", response_model=Data)
async def write_data(data: Data):
    result = await crud.write_data(data)
    if result is None:
        raise HTTPException(status_code=400, detail="Phone number already exists")
    return result


@router.put('/update_data', response_model=Data)
async def update_data(data: Data):
    result = await crud.update_data(data)
    if result is None:
        raise HTTPException(status_code=400, detail="Phone number not found")
    return result

#TODO покрыть тестами ручки
