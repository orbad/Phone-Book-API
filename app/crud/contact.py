from sqlalchemy.orm import Session
from typing import Optional
from schemas import schemas
from models import models

def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(
        first_name=contact.first_name,
        last_name=contact.last_name,
        phone_number=contact.phone_number,
        address=contact.address,
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def search_contacts(db: Session, phone_number: Optional[str] = None,first_name: Optional[str] = None, last_name: Optional[str] = None, address: Optional[str] = None):
    query = db.query(models.Contact)
    # Apply filters only if the values are provided
    if phone_number:
        query = query.filter(phone_number == models.Contact.phone_number)
    if first_name:
        query = query.filter(first_name == models.Contact.first_name)
    if last_name:
        query = query.filter(last_name == models.Contact.last_name)
    if address:
        query = query.filter(address == models.Contact.address)

    return query.all()

def get_contacts(db: Session, offset: int = 0, limit: int = 10):
    return db.query(models.Contact).offset(offset).limit(limit).all()

def update_contact(db: Session, phone_number: str, contact_update: schemas.ContactUpdate):
    db_contact = db.query(models.Contact).filter(phone_number == models.Contact.phone_number).first()
    if not db_contact:
        return None

    # Update only the fields that are provided
    if contact_update.first_name is not None:
        db_contact.first_name = contact_update.first_name
    if contact_update.last_name is not None:
        db_contact.last_name = contact_update.last_name
    if contact_update.phone_number is not None:
        db_contact.phone_number = contact_update.phone_number
    if contact_update.address is not None:
        db_contact.address = contact_update.address
    db.commit()
    db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, phone_number: str):
    db_contact = db.query(models.Contact).filter(phone_number == models.Contact.phone_number).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact
