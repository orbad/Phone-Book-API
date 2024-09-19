from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Contact(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    address: str

contacts = {
    "0544605039": Contact(first_name="Or", last_name="Test1", phone_number="0544605039", address="Shmorack 18, Holon", id=0),
    "0525745672": Contact(first_name="Or", last_name="Test2", phone_number="0525745672", address="Igal Alon 20, Tel Aviv", id=1),
    "054630003": Contact(first_name="Omri", last_name="Kash", phone_number="054630003", address="Petach Tikva", id=2)
}

@app.get("/")
def index() -> dict[str, dict[str, Contact]]:
    return {"contacts": contacts}

@app.get("/phonebook/search/{phone}")
def query_contact_by_phone_number(phone: str) -> Contact:
    if phone not in contacts:
        raise HTTPException(status_code=404, detail=f"The contact with phone number {phone} is not found.")
    return contacts[phone]


@app.post("/")
def add_contact(contact: Contact) -> dict[str, Contact]:
    if contact.phone_number in contacts:
        HTTPException(status_code=400, detail=f"A contact with the phone number {contact.phone_number} already exists.")

    contacts[contact.phone_number] = contact
    return {"added": contact}

@app.put("/update/{phone_number}")
def update(
        phone_number: str,
        first_name: str | None = None,
        last_name: str | None = None,
        address: str | None =None
) -> dict[str, Contact]:
    if phone_number not in contacts:
        HTTPException(status_code=404, detail=f"Contact with {phone_number=} does not exist.")
    if all(info is None for info in (first_name, last_name, address)):
        raise HTTPException(
            status_code=400, detail=f"No parameters provided for update."
         )
    contact = contacts[phone_number]
    if first_name is not None:
        contact.first_name = first_name
    if last_name is not None:
        contact.last_name = last_name
    if address is not None:
        contact.address = address

    return {"Updated": contact}


@app.delete("/delete/{phone_number}")
def delete_contact(phone_number: str) -> dict[str, Contact]:

    if phone_number not in contacts:
        raise HTTPException(
            status_code=404, detail=f"Contact with {phone_number=} does not exist."
        )
    contact = contacts.pop(phone_number)
    return {"Deleted contact": contact}

