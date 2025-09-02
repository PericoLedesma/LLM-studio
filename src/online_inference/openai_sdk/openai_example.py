from openai import OpenAI
import os

openai_api_key = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Write a short story"}]
)
print(response.choices[0].message.content)