from pydantic import BaseModel, constr, Field
from typing import Optional

class ContactCreate(BaseModel):
    first_name: constr(min_length=1, max_length=255)
    last_name: constr(min_length=1, max_length=255)
    phone_number: str = Field(pattern='^\d{1,14}$') # Verifies it's a number between 1 to 14 digits
    address: constr(min_length=1, max_length=255)

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

# Contact Model without ID (used for responses)
class ContactWithoutID(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    address: str

class Config:
    from_attributes = True
