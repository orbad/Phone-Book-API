from enum import Enum
from fastapi import FastAPI, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session
from db import models, schemas
from db.session import SessionLocal, engine
from db.models import Base
from crud import contact as crud_contact
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
from typing import Optional

logger.debug("Starting FastAPI app...")
Base.metadata.create_all(bind=engine)
logger.debug("Database setup completed.")
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a contact
@app.post("/contacts/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    try:
        db_contact = crud_contact.create_contact(db=db, contact=contact)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail="Invalid phone number: must be between 1 and 14 digits.")
    return db_contact

# Get a contact by ID
@app.get("/contacts/search", response_model=list[schemas.Contact])
def search_contacts(
        phone_number: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        address: Optional[str] = None,
        db: Session = Depends(get_db)
):
    contacts = crud_contact.search_contacts(db=db, phone_number=phone_number, first_name=first_name, last_name=last_name, address=address)
    if not contacts:
        raise HTTPException(status_code=404, detail="No contacts found")
    return contacts

# Get all contacts
@app.get("/contacts/", response_model=list[schemas.Contact])
def read_contacts(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    contacts = crud_contact.get_contacts(db=db, offset=offset, limit=limit)
    return contacts

# Update a contact by ID
@app.put("/contacts/{phone_number}", response_model=schemas.Contact)
def update_contact(phone_number: str, contact: schemas.ContactUpdate, db: Session = Depends(get_db)):
    updated_contact = crud_contact.update_contact(db=db, phone_number=phone_number, contact_update=contact)
    if updated_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact

# Delete a contact by ID
@app.delete("/contacts/{phone_number}", response_model=schemas.Contact)
def delete_contact(phone_number: str, db: Session = Depends(get_db)):
    db_contact = crud_contact.delete_contact(db=db, phone_number=phone_number)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# app = FastAPI()
#
# class Contact(BaseModel):
#     first_name: str
#     last_name: str
#     phone_number: str
#     address: str
#
# contacts = {
#     "0544605039": Contact(first_name="Or", last_name="Test1", phone_number="0544605039", address="Shmorack 18, Holon", id=0),
#     "0525745672": Contact(first_name="Or", last_name="Test2", phone_number="0525745672", address="Igal Alon 20, Tel Aviv", id=1),
#     "054630003": Contact(first_name="Omri", last_name="Kash", phone_number="054630003", address="Petach Tikva", id=2)
# }
#
# # @app.get("/")
# # def index() -> dict[str, dict[str, Contact]]:
# #     return {"contacts": contacts}
#
# # Get all contacts
# @app.get("/contacts/")
# def index() -> dict[str, dict[str, Contact]]:
#     return {"contacts": contacts}
#
# # Get a contact by phone number (GET method)
# @app.get("/contacts/{phone_number}")
# def query_contact_by_phone_number(phone_number: str) -> Contact:
#     if phone_number not in contacts:
#         raise HTTPException(status_code=404, detail=f"The contact with phone number {phone_number} is not found.")
#     return contacts[phone_number]
#
# # Add a new contact (POST method)
# @app.post("/contacts/")
# def add_contact(contact: Contact) -> dict[str, Contact]:
#     if contact.phone_number in contacts:
#         HTTPException(status_code=400, detail=f"A contact with the phone number {contact.phone_number} already exists.")
#
#     contacts[contact.phone_number] = contact
#     return {"added": contact}
#
# # Update a contact (PUT method)
# @app.put("/contacts/{phone_number}")
# def update(
#         phone_number: str,
#         first_name: str | None = None,
#         last_name: str | None = None,
#         address: str | None =None
# ) -> dict[str, Contact]:
#     if phone_number not in contacts:
#         HTTPException(status_code=404, detail=f"Contact with {phone_number=} does not exist.")
#     if all(info is None for info in (first_name, last_name, address)):
#         raise HTTPException(
#             status_code=400, detail=f"No parameters provided for update."
#         )
#     contact = contacts[phone_number]
#     if first_name is not None:
#         contact.first_name = first_name
#     if last_name is not None:
#         contact.last_name = last_name
#     if address is not None:
#         contact.address = address
#
#     return {"Updated": contact}
#
#
# @app.delete("/contacts/{phone_number}")
# def delete_contact(phone_number: str) -> dict[str, Contact]:
#
#     if phone_number not in contacts:
#         raise HTTPException(
#             status_code=404, detail=f"Contact with {phone_number=} does not exist."
#         )
#     contact = contacts.pop(phone_number)
#     return {"Deleted contact": contact}
