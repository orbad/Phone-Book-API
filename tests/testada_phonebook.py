import requests
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from db.session import SessionLocal
from crud import contact as crud_contact
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Starting FastAPI app...")
logger.debug("Database setup completed.")


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def main():
    # Base API URL
    api_url = "http://127.0.0.1:8000/contacts/"

    # Initial GET request to see the current state of contacts
    print("Initial state of contacts:")
    initial_contacts = requests.get(api_url).json()
    print(initial_contacts)

    # 1. Add a new contact
    for i in range(1, 10):
        print("\nAdding a new contact:")
        new_contact = {
            "first_name": "Or",
            "last_name": "Badani",
            "phone_number": f"+972544605039{i}",
            "address": "Nowhere"
        }
        response = requests.post(api_url, json=new_contact)
        print(response.json())

    # 2. Query the newly added contact by phone number
    print("\nQuerying the newly added contact by phone number:")
    phone_number = new_contact["phone_number"]
    response = requests.get(f"{api_url}search?phone_number={phone_number}")
    print(response.json())

    # 3. Update the contact's first name
    print("\nUpdating the contact's first name:")
    contact = {
        "first_name": "Hola",
        "last_name": "Senior!",
        "phone_number": f"059525219123{i}",
        "address": "Nowhere"
    }
    update_url = f"{api_url}{phone_number}"
    response = requests.put(update_url)
    print(response.json())

    # 4. Query the updated contact
    print("\nQuerying the updated contact by phone number:")
    response = requests.get(f"{api_url}search?phone_number={phone_number}")
    print(response.json())

    # # 5. Attempt to update the contact with no parameters (should fail)
    # print("\nAttempting to update the contact with no parameters (should fail):")
    # response = requests.put(f"{api_url}{phone_number}")
    # print(response.status_code)
    # print(response.json())

    # 6. Delete the contact
    print("\nDeleting the contact:")
    response = requests.delete(f"{api_url}{phone_number}")
    print(response.json())

    # 7. Attempt to query the deleted contact (should return 404)
    print("\nQuerying the deleted contact (should return 404):")
    response = requests.get(f"{api_url}search?phone_number={phone_number}")
    print(response.status_code)
    print(response.json())


if __name__ == "__main__":
    main()
