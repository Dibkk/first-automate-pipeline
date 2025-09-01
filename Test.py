#Client side

import json
import requests

URL = "http://127.0.0.1:5000/emps"
# response=requests.get(URL)
# print(response.json())

# data = {
#         "name": "Hito",
#         "age": 20,
#         "email": "kook@example.com",
#         "Department": "Chef"
#     }
# response=requests.post(URL,json=data)
# print("POST status:", response.status_code, response.text)

print("\n")

response = requests.get(URL)
print("POST status:", response.status_code, response.text)
