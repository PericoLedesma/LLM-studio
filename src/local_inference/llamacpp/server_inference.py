# Create a api endpoint to call the model server (llama-server -model xxx)

import requests

response = requests.post(
    "http://localhost:8080/completion",
    json={
        "prompt": "Write a haiku about AI and nature",
        "n_predict": 64
    }
)

# print(response.json())
print(response.json().keys())
print("----")
print(response.json()['content'])