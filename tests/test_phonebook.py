import requests

import app.main
num_of_contacts = len(app.main.contacts)
print(requests.get("http://127.0.0.1:8000/").json())
for i in range(num_of_contacts):
    print(requests.get(f"http://127.0.0.1:8000/phonebook/search/{i}").json())

print(requests.get(f"http://127.0.0.1:8000/phonebook/search/{num_of_contacts}").json())
