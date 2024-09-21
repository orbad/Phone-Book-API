import pytest
import requests

API_URL = "http://127.0.0.1:8000/contacts/"

@pytest.fixture
def contact_data():
    return {
        "first_name": "Or",
        "last_name": "Badani",
        "phone_number": "054460503999",
        "address": "Nowhere"
    }

def test_get_contacts():
    # Test the initial GET request
    response = requests.get(API_URL)
    assert response.status_code == 200
    contacts = response.json()
    assert isinstance(contacts, list)  # Make sure we get a list of contacts

def test_add_contact(contact_data):
    # Test adding a new contact
    response = requests.post(API_URL, json=contact_data)
    assert response.status_code == 200  # Created
    contact = response.json()
    assert contact["phone_number"] == contact_data["phone_number"]

def test_query_contact(contact_data):
    # Test querying the contact by phone number
    phone_number = contact_data["phone_number"]
    search_url = f"{API_URL}search?phone_number={phone_number}"
    response = requests.get(search_url)
    assert response.status_code == 200
    contact = response.json()[0]  # Should return a list with one contact
    assert contact["phone_number"] == phone_number

def test_update_contact(contact_data):
    # Test updating the contact
    phone_number = contact_data["phone_number"]
    update_url = f"{API_URL}{phone_number}"
    updated_contact = {
        "first_name": "OrUpdated",
        "last_name": "Badani",
        "phone_number": phone_number,
    }
    response = requests.put(update_url, json=updated_contact)
    assert response.status_code == 200
    contact = response.json()
    contact_data = contact
    assert contact["first_name"] == "OrUpdated"

def test_delete_contact(contact_data):
    # Test deleting the contact
    phone_number = contact_data["phone_number"]
    delete_url = f"{API_URL}{phone_number}"
    response = requests.delete(delete_url)
    assert response.status_code == 200
    assert response.json() == contact_data

    # Verify that the contact is really deleted
    search_url = f"{API_URL}search?phone_number={phone_number}"
    response = requests.get(search_url)
    assert response.status_code == 404