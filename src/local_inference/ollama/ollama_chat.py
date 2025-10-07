import ollama

messages = [
    {
        'role': 'system',
        'content': 'you only talk like a 1950s gangster, and you limit your responses to 20 words'
    },
    {
        'role': 'user',
        'content': 'why is the sky blue?'
    }
]

response = ollama.chat(model='llama3', messages=messages)

print(response['message']['content'])