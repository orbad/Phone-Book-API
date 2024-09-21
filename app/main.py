import logging
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, Request, Response
from pydantic import ValidationError
from sqlalchemy.orm import Session

from db.session import Base, engine, get_db
from schemas import schemas
from crud import contact as crud_contact
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

import logging, time
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
from typing import Optional

logger.debug("Starting FastAPI app...")
Base.metadata.create_all(bind=engine)
logger.debug("Database setup completed.")
app = FastAPI()

# Define Prometheus metrics
REQUEST_COUNT = Counter(
    "request_count", "App Request Count",
    ["app_name", "method", "endpoint", "http_status"]
)

REQUEST_LATENCY = Histogram(
    "request_latency_seconds", "Request latency",
    ["app_name", "endpoint"]
)

APP_NAME = "phonebook_api"

# Middleware to collect metrics
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    REQUEST_LATENCY.labels(APP_NAME, request.url.path).observe(process_time)
    REQUEST_COUNT.labels(APP_NAME, request.method, request.url.path, response.status_code).inc()

    return response

# Metrics endpoint
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# Create a contact
@app.post("/contacts/", response_model=schemas.ContactWithoutID)
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
@app.get("/contacts/search", response_model=list[schemas.ContactWithoutID])
def search_contacts(
        phone_number: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        address: Optional[str] = None,
        db: Session = Depends(get_db)
):
    if all(param is None for param in [phone_number, first_name, last_name, address]):
        raise HTTPException(status_code=400, detail="At least one search parameter must be provided.")

    contacts = crud_contact.search_contacts(db=db, phone_number=phone_number, first_name=first_name, last_name=last_name, address=address)
    return contacts

# Get all contacts
@app.get("/contacts/", response_model=list[schemas.ContactWithoutID])
def read_contacts(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    contacts = crud_contact.get_contacts(db=db, offset=offset, limit=limit)
    return contacts

# Update a contact by ID
@app.put("/contacts/{phone_number}", response_model=schemas.ContactWithoutID)
def update_contact(phone_number: str, contact: schemas.ContactUpdate, db: Session = Depends(get_db)):
    db_contact = crud_contact.search_contacts(db, phone_number=phone_number)
    if db_contact is None or len(db_contact) == 0:
        raise HTTPException(status_code=404, detail="Contact not found")
    else:
        db_contact = db_contact[0]
    if all(
            value is None for value in (contact.first_name, contact.last_name, contact.phone_number, contact.address)
    ):
        raise HTTPException(
            status_code=400, detail="No parameters provided for update."
        )
    updated_contact = crud_contact.update_contact(db=db, phone_number=phone_number, contact_update=contact)
    return updated_contact

# Delete a contact by ID
@app.delete("/contacts/{phone_number}", response_model=schemas.ContactWithoutID)
def delete_contact(phone_number: str, db: Session = Depends(get_db)):
    db_contact = crud_contact.delete_contact(db=db, phone_number=phone_number)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact