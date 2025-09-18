
import os
import pandas as pd
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather_by_city",
        "description": "It gives back the weather of a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The name of the city to get weather for.",
                },
                "weather": {
                    "type": "string",
                    "description": "The weather in the city.",
                    "enum": ["sunny", "rainy"],
                }
            },
            "required": ["city"]
        }
    }
}

messages0 = [{"role": "user",
             "content": "What tools do you have?"}]

messages1 = [{"role": "user",
             "content": "What's the weather like in Paris?"}]

messages2 = [{"role": "system", "content": "You are a helpful assistant. Use the tools when relevant. Get to the answer "},
             {"role": "user", "content": "What's the weather like in Paris?"}]

messages3 = [{"role": "system", "content": "You are a helpful assistant. Use the tools when relevant. Get to the answer "},
             {"role": "user", "content": "Say hello"}]

response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=messages3,
    tools=[weather_tool],
    # tool_choice="auto"  # auto is default, but we'll be explicit
)
print("Message content")
print(response.choices[0].message.content)
print("---")
print("Tools called:")
print(response.choices[0].message.tool_calls)
print("---")
if response.choices[0].message.tool_calls:
    print("Function call")
    print(response.choices[0].message.tool_calls[0].function.name)
    print(response.choices[0].message.tool_calls[0].function.arguments)
else:
    print("No function called")