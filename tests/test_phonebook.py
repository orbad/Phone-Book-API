import pytest
import requests
from multiprocessing.dummy import Pool as ThreadPool

API_URL = "http://127.0.0.1:8000/contacts/"


@pytest.fixture
def contact_data():
    return {
        "first_name": "Or",
        "last_name": "Badani",
        "phone_number": "0544605039",
        "address": "Nowhere"
    }


def test_get_contacts():
    """Test retrieving all contacts."""
    response = requests.get(API_URL)
    assert response.status_code == 200
    contacts = response.json()
    assert isinstance(contacts, list)


def test_add_contact(contact_data):
    """Test adding a new contact."""
    response = requests.post(API_URL, json=contact_data)
    assert response.status_code == 200
    contact = response.json()
    assert contact["phone_number"] == contact_data["phone_number"]


def test_add_duplicate_contact(contact_data):
    """Test adding a duplicate contact."""
    response = requests.post(API_URL, json=contact_data)
    assert response.status_code == 400  # Bad Request
    error = response.json()
    assert "already exists" in error["detail"]


@pytest.mark.parametrize("invalid_data, error_detail", [
    ({"first_name": "", "phone_number": "1234567890"}, "first_name"),
    ({"first_name": "John", "phone_number": ""}, "phone_number"),
    ({"first_name": "John", "phone_number": "abc"}, "phone_number"),
    ({"first_name": "John", "phone_number": "123456789012345"}, "phone_number"),  # Exceeds max length
])
def test_add_contact_invalid_data(invalid_data, error_detail):
    """Test adding a contact with invalid data."""
    response = requests.post(API_URL, json=invalid_data)
    assert response.status_code == 422  # Unprocessable Entity
    errors = response.json()
    assert any(error_detail in str(err["loc"]) for err in errors["detail"])


def test_query_contact(contact_data):
    """Test querying the contact by phone number."""
    phone_number = contact_data["phone_number"]
    search_url = f"{API_URL}search?phone_number={phone_number}"
    response = requests.get(search_url)
    assert response.status_code == 200
    contacts = response.json()
    assert len(contacts) == 1
    contact = contacts[0]
    assert contact["phone_number"] == phone_number


def test_query_nonexistent_contact():
    """Test querying a contact that doesn't exist."""
    search_url = f"{API_URL}search?phone_number=0000000000"
    response = requests.get(search_url)
    assert response.status_code == 404  # Not Found


def test_update_contact(contact_data):
    """Test updating the contact."""
    phone_number = contact_data["phone_number"]
    update_url = f"{API_URL}{phone_number}"
    updated_contact = {
        "first_name": "OrUpdated",
        "last_name": "BadaniUpdated",
        "address": "Somewhere"
    }
    response = requests.put(update_url, json=updated_contact)
    assert response.status_code == 200
    contact = response.json()
    assert contact["first_name"] == "OrUpdated"
    assert contact["last_name"] == "BadaniUpdated"
    assert contact["address"] == "Somewhere"


def test_update_nonexistent_contact():
    """Test updating a contact that doesn't exist."""
    update_url = f"{API_URL}0000000000"
    updated_contact = {
        "first_name": "NoOne",
    }
    response = requests.put(update_url, json=updated_contact)
    assert response.status_code == 404  # Not Found


def test_delete_contact(contact_data):
    """Test deleting the contact."""
    phone_number = contact_data["phone_number"]
    delete_url = f"{API_URL}{phone_number}"
    response = requests.delete(delete_url)
    assert response.status_code == 200
    contact = response.json()
    assert contact["phone_number"] == phone_number

    # Verify that the contact is really deleted
    search_url = f"{API_URL}search?phone_number={phone_number}"
    response = requests.get(search_url)
    assert response.status_code == 404


def test_delete_nonexistent_contact():
    """Test deleting a contact that doesn't exist."""
    delete_url = f"{API_URL}0000000000"
    response = requests.delete(delete_url)
    assert response.status_code == 404  # Not Found


def test_method_not_allowed():
    """Test method not allowed responses."""
    response = requests.patch(API_URL)
    assert response.status_code == 405  # Method Not Allowed


def test_add_contact_missing_fields():
    """Test adding a contact with missing required fields."""
    incomplete_data = {
        "phone_number": "1234567890"
    }
    response = requests.post(API_URL, json=incomplete_data)
    assert response.status_code == 422  # Unprocessable Entity


def test_search_contacts_by_first_name(contact_data):
    """Test searching contacts by first name."""
    first_name = contact_data["first_name"]
    search_url = f"{API_URL}search?first_name={first_name}"
    response = requests.get(search_url)
    assert response.status_code == 200
    contacts = response.json()
    assert any(contact["first_name"] == first_name for contact in contacts)


def test_pagination():
    """Test pagination parameters."""
    params = {'offset': 0, 'limit': 2}
    response = requests.get(API_URL, params=params)
    assert response.status_code == 200
    contacts = response.json()
    assert len(contacts) <= 2


def test_concurrent_requests(contact_data):
    """Test handling of concurrent requests."""

    def make_request(data):
        return requests.post(API_URL, json=data)

    contact_data_list = [
        {**contact_data, "phone_number": f"054460503{i}"} for i in range(10)
    ]

    pool = ThreadPool(5)
    responses = pool.map(make_request, contact_data_list)
    pool.close()
    pool.join()

    for response in responses:
        assert response.status_code == 200

    # Cleanup
    for data in contact_data_list:
        delete_url = f"{API_URL}{data['phone_number']}"
        requests.delete(delete_url)


def test_long_strings():
    """Test adding a contact with excessively long strings."""
    long_string = "a" * 300  # Exceeds typical VARCHAR(255) limit
    invalid_data = {
        "first_name": long_string,
        "last_name": long_string,
        "phone_number": "1234567890",
        "address": long_string
    }
    response = requests.post(API_URL, json=invalid_data)
    assert response.status_code == 422  # Unprocessable Entity


def test_special_characters():
    """Test adding a contact with special characters."""
    special_chars = "!@#$%^&*()_+{}:\"<>?[];',./`~"
    contact_data_special = {
        "first_name": special_chars,
        "last_name": special_chars,
        "phone_number": "0987654321",
        "address": special_chars
    }
    response = requests.post(API_URL, json=contact_data_special)
    assert response.status_code == 200

    # Cleanup
    delete_url = f"{API_URL}{contact_data_special['phone_number']}"
    requests.delete(delete_url)


def test_numeric_names():
    """Test adding a contact with numeric names."""
    contact_data_numeric = {
        "first_name": "123",
        "last_name": "456",
        "phone_number": "1122334455",
        "address": "789"
    }
    response = requests.post(API_URL, json=contact_data_numeric)
    assert response.status_code == 200

    # Cleanup
    delete_url = f"{API_URL}{contact_data_numeric['phone_number']}"
    requests.delete(delete_url)


def test_empty_strings():
    """Test adding a contact with empty strings."""
    empty_data = {
        "first_name": "",
        "last_name": "",
        "phone_number": "2233445566",
        "address": ""
    }
    response = requests.post(API_URL, json=empty_data)
    assert response.status_code == 422  # Unprocessable Entity


def test_invalid_phone_number_format():
    """Test adding a contact with invalid phone number format."""
    invalid_phone_data = {
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "phone123",
        "address": "Address"
    }
    response = requests.post(API_URL, json=invalid_phone_data)
    assert response.status_code == 422  # Bad Request


def test_search_with_no_parameters():
    """Test searching without any parameters."""
    search_url = f"{API_URL}search"
    response = requests.get(search_url)
    assert response.status_code == 404  # Bad Request


def test_update_contact_no_fields():
    """Test updating a contact without providing any fields."""
    phone_number = "0544605039"
    update_url = f"{API_URL}{phone_number}"
    response = requests.put(update_url, json={})
    assert response.status_code == 404  # Not Found


def test_sql_injection_attempt():
    """Test for SQL injection vulnerability."""
    malicious_data = {
        "first_name": "John'; DROP TABLE contacts; --",
        "last_name": "Doe",
        "phone_number": "3344556677",
        "address": "Unknown"
    }
    response = requests.post(API_URL, json=malicious_data)
    assert response.status_code == 200

    # Verify that the contacts table still exists
    response = requests.get(API_URL)
    assert response.status_code == 200

    # Cleanup
    delete_url = f"{API_URL}{malicious_data['phone_number']}"
    requests.delete(delete_url)


def test_large_number_of_contacts():
    """Test adding a large number of contacts."""
    contact_data_list = [
        {
            "first_name": f"FirstName{i}",
            "last_name": f"LastName{i}",
            "phone_number": f"077{1000000 + i}",
            "address": f"Address{i}"
        } for i in range(100)
    ]
    try:
        for data in contact_data_list:
            response = requests.post(API_URL, json=data)
            assert response.status_code == 200

            # Retrieve contacts using pagination
            total_contacts_retrieved = []
            offset = 0
            limit = 10

        while True:
            params = {'offset': offset, 'limit': limit}
            response = requests.get(API_URL, params=params)
            assert response.status_code == 200
            contacts = response.json()
            if not contacts:
                break
            total_contacts_retrieved.extend(contacts)
            offset += limit

        # Verify total contacts retrieved
        assert len(total_contacts_retrieved) >= 100

    finally:
        # Cleanup
        for data in contact_data_list:
            delete_url = f"{API_URL}{data['phone_number']}"
            requests.delete(delete_url)
