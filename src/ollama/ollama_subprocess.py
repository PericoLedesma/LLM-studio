import subprocess

def chat_with_ollama(prompt):
    # Start the Ollama process
    process = subprocess.Popen(
        ['ollama', 'run', 'llama3'],  # Replace 'llama3' with your model name
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Send the prompt to Ollama
    stdout, stderr = process.communicate(input=prompt)

    if process.returncode != 0:
        raise Exception(f"Error: {stderr.strip()}")

    return stdout.strip()


# Example usage
response = chat_with_ollama("Hello, how are you?")
print("Ollama response:", response)