# llama.cpp and the LLaMA Ecosystem

| Component               | Layer       | Purpose / Description                                                                      | Typical Use Case                                                 |
|-------------------------|-------------|--------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| **llama-cpp-python**    | Low-level   | Python bindings for `llama.cpp`. Allows loading and running GGUF models from Python        | Python projects needing direct control over model inference      |
| **llama-cli**           | CLI         | Command-line interface for `llama.cpp` to run models interactively or with prompts         | Quick local testing and interactive chat in terminal             |
| **llama-server**        | Service/API | REST API wrapper around `llama.cpp` for server mode usage                                  | Exposing LLaMA models via HTTP/REST API                          |
| **llama-stack**         | Mid-level   | Meta’s reference architecture for building LLaMA-powered applications (API, memory, tools) | Building full LLaMA apps or servers with orchestration           |
| **llama (PyPI / Meta)** | High-level  | Official Python SDK for interacting with LLaMA models and stack; abstracts backends        | Easy API-style interaction with LLaMA models for apps or scripts |

# What is llama.cpp?

`llama.cpp` is a lightweight, high-performance **C++ library** for running LLaMA and other GGUF-compatible language models locally.

**Key Features:**

* ⚡ Supports **CPU-only inference** and **GPU acceleration** via Metal on Apple devices
* 🧠 Enables **fast, low-memory execution** of large language models
* 🔒 Runs models **locally**, no cloud required

Perfect for **local experimentation, research, and integration** into apps that need efficient language model inference.

---


### What happens if you don’t use llama.cpp?

- You’d have to write your own loader to read `consolidated.00.pth` and apply `params.json`.  
- You’d need a heavy framework (PyTorch/TF) and GPU drivers to run efficiently.  
- You’d miss out on the GGML quantization and CPU optimizations.  
- You’d have to handle tokenization yourself (though Hugging Face’s `transformers` can help).  
- Your deployment would be bulkier, slower to start, and harder to port to non-Python environments.


### Getting Started with llama.cpp
Follow these steps to install, download a model, and run `llama.cpp` on your system.
----

#### 1. Install llama.cpp
```bash
  brew install llama.cpp
```
Verify that the llama tool is installed:
```bash
  which llama
```

#### 2. Get a GGUF Model

Example: Llama 3 8B Instruct:

```bash
    mkdir ~/llama_models
    cd ~/llama_models
    curl -L -o llama3-8b-instruct.gguf https://huggingface.co/meta-llama/Llama-3-8B-Instruct-GGUF/resolve/main/llama-3-8b-instruct.Q4_K_M.gguf
```
#### 3. Run the Model
From the command line:
```bash
  llama-cli -m ~/llama_models/llama3-8b-instruct.gguf -p "Write a poem"
```
Or from Python using `llama-cpp-python`:
``` python
    from llama_cpp import Llama

    # Load a GGUF model
    llm = Llama(model_path="/Users/pedrorodriguezdeledesmajimenez/scripts/llm_models/mistral-7b-instruct-v0.2.Q4_K_M.gguf")
    
    # Run inference
    output = llm("Write a haiku about Python", max_tokens=64)
    print(output["choices"][0]["text"])
```

#### 4. Useful Settings

```bash
  # Para limitar el uso de memoria
  llama -m ~/llama_models/llama3-8b-instruct.gguf --memory_f16

  # Acelerar usando Metal (GPU):
llama-cli -m ~/llama_models/llama-3-8b-instruct.Q4_K_M.gguf -ngl 999

  # Cambiar el número de tokens generados
  llama -m ~/llama_models/llama3-8b-instruct.gguf -n 256
```

#### 5. Activate API mode
Run llama.cpp as a server to expose a local API:
``` bash
llama-server
```
You can now send requests to the API endpoint (default: http://localhost:8080).

#### 6. Send an API Request

You can send a prompt to the server via curl:
```bash
    curl http://localhost:8080/completion \
      -H "Content-Type: application/json" \
      -d '{
        "prompt": "Write a haiku about AI and nature",
        "n_predict": 64
      }'
```

Or from Python using requests:
```python
    import requests
    
    response = requests.post(
        "http://localhost:8080/completion",
        json={
            "prompt": "Write a haiku about AI and nature",
            "n_predict": 64
        }
    )
    
    print(response.json())
```







