from pydantic import BaseModel, field_validator
import re


# Phone model
class Phone(BaseModel):
    phone: str

    @field_validator("phone")
    def val_phone(cls, value: str) -> str:
        if not re.match(r'^[\+|8][1-9][0-9]{7,14}$', value): # regex for checking phone number (probably not perfect)
            raise ValueError("Invalid phone number")
        if re.match(r"^8\d{10}$", value): # determining if phone number is in russian format
            value = value.replace("8", "+7", 1)

        return value

# Data model
class Data(Phone):
    address: str
