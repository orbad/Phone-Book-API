import requests
from fastapi.logger import logger

import app.main
num_of_contacts = len(app.main.contacts)
api_url = "http://127.0.0.1:8000/"
print(requests.get(api_url).json())

print("Adding a contact:")
response = requests.post(api_url, json={
    "first_name": "Hola",
    "last_name": "Senior!",
    "phone_number": "0525252521",
    "address": "Nowhere"
})
print(response.json())

print(requests.get(api_url).json())
# for i in range(num_of_contacts):
#     print(requests.get(api_url+f"/phonebook/search/{i}").json())

print(requests.get(api_url+f"/phonebook/search/{num_of_contacts}").json())

print("Updating a contact:")
print(requests.put(api_url+"update/0544605039?first_name=Toga"))
print(requests.get(api_url).json())
print()

print("Deleting a contact:")
print(requests.delete(api_url+"delete/0544605039"))
print(requests.get(api_url).json())
print()
