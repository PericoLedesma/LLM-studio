import json
import os
from turtle import pensize

import requests
from openai import OpenAI
from pydantic import BaseModel, Field

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

"""
docs: https://platform.openai.com/docs/guides/function-calling
"""

# --------------------------------------------------------------
# Define the tool (function) that we want to call
# --------------------------------------------------------------


def get_weather(latitude, longitude):
    """This is a publically available API that returns the weather for a given location."""
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )
    data = response.json()
    return data["current"]


# --------------------------------------------------------------
# Step 1: Call model with get_weather tool defined
# --------------------------------------------------------------

# Define the tools that we want to call
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current temperature for provided coordinates in celsius.",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"},
                },
                "required": ["latitude", "longitude"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }
]

# Define the messages that we want to send to the model
system_prompt = "You are a helpful weather assistant."

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "What's the weather like in Paris today?"},
]
print("--------------------------------")
print("Messages to the model: ", messages)
print("--------------------------------")

# Call the model
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
)

# --------------------------------------------------------------
# Step 2: Model decides to call function(s)
# --------------------------------------------------------------

print("--------------------------------")
print("Answer from the model: ", completion.model_dump())
print("--------------------------------")
completion.model_dump()

# --------------------------------------------------------------
# Step 3: Execute get_weather function
# --------------------------------------------------------------
print("Tools called: ", completion.choices[0].message.tool_calls)

# Define the function that we want to call
def call_function(name, args):
    if name == "get_weather":
        print("Calling get_weather function")
        return get_weather(**args)

# Execute the function
for tool_call in completion.choices[0].message.tool_calls:
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    messages.append(completion.choices[0].message)

    result = call_function(name, args)
    messages.append(
        {"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result)}
    )

print("--------------------------------")
print("Messages to model: ", messages)
print("--------------------------------")

# --------------------------------------------------------------
# Step 4: Supply result and call model again
# --------------------------------------------------------------


class WeatherResponse(BaseModel):
    temperature: float = Field(
        description="The current temperature in celsius for the given location."
    )
    response: str = Field(
        description="A natural language response to the user's question."
    )


completion_2 = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    response_format=WeatherResponse,
)
print("--------------------------------")
print("Completion 2: ", completion_2)
print("--------------------------------")

# --------------------------------------------------------------
# Step 5: Check model response
# --------------------------------------------------------------

final_response = completion_2.choices[0].message.parsed
final_response.temperature
final_response.response

print("--------------------------------")
print("Final Response: ", final_response)
print("--------------------------------")
print("Temperature: ", final_response.temperature)
print("Response: ", final_response.response)
print("--------------------------------")