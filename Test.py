#Client side

import json
import requests

URL = "http://127.0.0.1:5000/emps"
# response=requests.get(URL)
# print(response.json())

# data = {
#             "name":"Hito",
#             "age":20,
#             "email":"Kook@gmail.com",
#             "Department":"Chef"
#         }
# response=requests.post(URL,json.dumps(data))

response=requests.get(URL)
print(response.json())
