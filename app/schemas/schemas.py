from pydantic import BaseModel, constr
from typing import Optional

class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    phone_number: constr(min_length=1, max_length=14)# Verifies it's between 1 to 14 (country_prefix + mobile)digits
    address: str

class ContactUpdate(ContactCreate):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

class Contact(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone_number: str
    address: str

    class Config:
        from_attributes = True
