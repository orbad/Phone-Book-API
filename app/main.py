from fastapi import FastAPI, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session
from db.session import Base
from schemas import schemas
from db.session import SessionLocal, engine
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
    existing_contact = crud_contact.search_contacts(db, phone_number=contact.phone_number)
    if existing_contact:
        raise HTTPException(
            status_code=400,
            detail=f"A contact with the phone number {contact.phone_number} already exists."
        )
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
    db_contact = crud_contact.search_contacts(db, phone_number=phone_number)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    if all(
            value is None for value in (contact.first_name, contact.last_name, contact.address)
    ):
        raise HTTPException(
            status_code=400, detail="No parameters provided for update."
        )
    updated_contact = crud_contact.update_contact(db=db, phone_number=phone_number, contact_update=contact)
    return updated_contact

# Delete a contact by ID
@app.delete("/contacts/{phone_number}", response_model=schemas.Contact)
def delete_contact(phone_number: str, db: Session = Depends(get_db)):
    db_contact = crud_contact.delete_contact(db=db, phone_number=phone_number)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact