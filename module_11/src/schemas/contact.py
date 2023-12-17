from typing import Optional
from datetime import date

from pydantic import BaseModel, EmailStr, Field


class ContactSchema(BaseModel):
    first_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=3, max_length=50)
    email: str = Field(min_length=3, max_length=100)
    phone_number: str = Field(min_length=3, max_length=20)
    date_of_birthday: date
    additional_information: str = Field(max_length=250)


class ContactUpdateSchema(ContactSchema):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    date_of_birthday: date
    additional_information: str


class ContactResponse(BaseModel):
    id: int = 1
    first_name: str
    last_name: str
    email: str
    phone_number: str
    date_of_birthday: date
    additional_information: str

    class Config:
        from_attributes = True
