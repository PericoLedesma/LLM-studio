# llama.cpp and the LLaMA Ecosystem

| Component              | Layer         | Purpose / Description                                                                 | Typical Use Case |
|------------------------|--------------|--------------------------------------------------------------------------------------|-----------------|
| **llama-cpp-python**   | Low-level    | Python bindings for `llama.cpp`. Allows loading and running GGUF models from Python | Python projects needing direct control over model inference |
| **llama-cli**          | CLI          | Command-line interface for `llama.cpp` to run models interactively or with prompts | Quick local testing and interactive chat in terminal |
| **llama-server**       | Service/API  | REST API wrapper around `llama.cpp` for server mode usage                             | Exposing LLaMA models via HTTP/REST API |
| **llama-stack**        | Mid-level    | Meta’s reference architecture for building LLaMA-powered applications (API, memory, tools) | Building full LLaMA apps or servers with orchestration |
| **llama (PyPI / Meta)**| High-level   | Official Python SDK for interacting with LLaMA models and stack; abstracts backends | Easy API-style interaction with LLaMA models for apps or scripts |

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

1. Install llama.cpp
```bash
  brew install llama.cpp
```
Localizar la herramienta `llama` en tu sistema:
```bash
  which llama
```

2. Consigue un modelo GGUF

llama.cpp no incluye modelos — necesitas descargar uno en formato GGUF.
Puedes bajarlo desde Hugging Face. Ejemplo: Llama 3 8B Instruct.

```bash
    mkdir ~/llama_models
    cd ~/llama_models
    curl -L -o llama3-8b-instruct.gguf https://huggingface.co/meta-llama/Llama-3-8B-Instruct-GGUF/resolve/main/llama-3-8b-instruct.Q4_K_M.gguf
```
3. Ejecuta el modelo

Una vez descargado, ejecuta:
```bash
  llama -m ~/llama_models/llama3-8b-instruct.gguf
```

4. Ajustes útiles

```bash
  # Para limitar el uso de memoria
  llama -m ~/llama_models/llama3-8b-instruct.gguf --memory_f16

  # Acelerar usando Metal (GPU):
llama-cli -m ~/llama_models/llama-3-8b-instruct.Q4_K_M.gguf -ngl 999

  # Cambiar el número de tokens generados
  llama -m ~/llama_models/llama3-8b-instruct.gguf -n 256


