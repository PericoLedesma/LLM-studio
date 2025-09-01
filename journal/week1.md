
# Ollama

Ollama is a tool designed for running and managing local large language models (LLMs) efficiently. 
It provides a simple interface to interact with models like LLaMA, enabling users to run them on their local machines without relying on external APIs.

---
## How It Works
Ollama operates by allowing users to download, install, and run various LLMs directly on their local hardware. It supports models in formats optimized for CPU inference, such as GGUF, making it accessible for users without high-end GPUs. The tool provides a command-line interface (CLI) for managing models and executing them with ease.
- **List Installed Models**
```bash
  ollama list
```

- **Search or Discover Available Models**: Ollama allows you to see available models for download
```bash
  ollama search <model-name>
```

- **Download/Install a New Model**
```bash
  ollama install <model-name>
```

- **Update an Existing Model**
```bash
  ollama update <model-name>
```

- **Running Models**
Once installed, you can run the model using a straightforward command. For instance, to start a session with the LLaMA model, you would use:
```bash
ollama run <model-name>
```

- **llama serve <model>**: This command starts a local server hosting the specified model, allowing you to interact with it via HTTP requests. This is useful for integrating the model into applications or services that can make API calls.
	•	This starts the model as a local server that listens for API requests.
	•	Useful if you want to integrate the model with apps or Python scripts.
	•	Once running, you can send prompts via HTTP requests instead of the terminal.
```bash
	ollama serve llama3 --port 5000
```

---
## **Integrate Ollama with Python scripts**: Ollama provides an interactive shell where you can input prompts and receive responses from the model in real-time.
To integrate Ollama with Python scripts, you can use Python's subprocess module to interact with the Ollama CLI. This allows you to send prompts to a locally running model and capture its responses programmatically. 

There are two main approaches:xx
1. Using subprocess in Python to call the Ollama CLI directly.
```python
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
```

In this example:
- subprocess.run: Executes the ollama run command with the specified model and prompt.
  - input=prompt: Sends the prompt to the model.
  - capture_output=True: Captures the model's response.
  - Error Handling: Ensures any errors during execution are caught and logged.

2. Using an HTTP Server 
Ollama can be exposed as a local API using a web framework like Flask:


```python
    from flask import Flask, request, jsonify
    import subprocess
    
    app = Flask(__name__)
    
    def query_ollama(prompt, model="llama3"):
        try:
            result = subprocess.run(
                ["ollama", "run", model],
                input=prompt,
                text=True,
                capture_output=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr.strip()}"
    
    @app.route('/query', methods=['POST'])
    def query():
        data = request.get_json()
        prompt = data.get("prompt", "")
        model = data.get("model", "llama3")
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
        response = query_ollama(prompt, model)
        return jsonify({"response": response})
    
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=1000)
```

Then you can query the model using curl:
```bash
curl -X POST http://localhost:1000/query \
-H "Content-Type: application/json" \
-d '{"prompt": "What is the capital of France?", "model": "llama3"}'
```


4. **H3. Key Features**
	•	Interactive Sessions: Chat directly with the model.
	•	Model Management: Switch between multiple models easily.
	•	Configurable: Adjust temperature, max tokens, etc.
	•	Integration: Works with Python, other scripts, and APIs.
	•	Local Storage: Runs without sending data to the cloud.
	•	Supported Formats: Works with modern LLM formats like GGUF for efficient inference.

3. **Interactive Sessions**: Ollama provides an interactive shell where you can input prompts and receive responses from the model in real-time.
4. **Configuration Options**: You can customize the behavior of the model using various flags and options provided by Ollama, such as setting the temperature for response variability.
5. **Model Management**: Ollama includes features for managing multiple models, allowing you to switch between them easily.
6. **Integration with Other Tools**: Ollama can be integrated with other applications and services, making it a versatile choice for developers looking to leverage local LMs.