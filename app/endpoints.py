from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
import logging

from app.models import Data, Phone

# logger
logger = logging.getLogger(__name__)


router = APIRouter()

# endpoint for writing and updating data
@router.post("/write_data", response_model=Data)
async def write_data(data: Data):

    return data
    #TODO прикрутить редис (запись данных)


@router.get("/check_data")
async def check_data(phone: str):
    # validation of phone number
    try:
        val_phone = Phone(phone=phone)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid phone number")
    
    return val_phone.phone
    #TODO прикрутить редис (чтение данных)