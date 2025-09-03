# What is llama.cpp?

`llama.cpp` is a lightweight, high-performance **C++ library** for running LLaMA and other GGUF-compatible language models locally.

**Key Features:**

* ⚡ Supports **CPU-only inference** and **GPU acceleration** via Metal on Apple devices
* 🧠 Enables **fast, low-memory execution** of large language models
* 🔒 Runs models **locally**, no cloud required

Perfect for **local experimentation, research, and integration** into apps that need efficient language model inference.


---

## Prepare llama.cpp

### Why llama.cpp?

**llama.cpp** is exactly that: a standalone, header-only C/C++ runtime optimized for LLaMA-style models. Here’s why it’s so useful for Llama 3:

- **No heavy Python/GPU stack required**  
  Run on plain CPUs (or via very light CUDA support) without installing PyTorch, TensorFlow, or any Python dependencies.

- **GGML quantization support**  
  Convert your `.pth` weights into its own compressed “GGML” format—trading off a bit of precision for huge memory and speed gains. You can even go down to 4- or 2-bit.

- **Cross-platform and embeddable**  
  Compile it to Windows, Linux, macOS—even mobile or WebAssembly—so you can embed inference into pretty much anything.

- **Fast startup and low overhead**  
  A small binary with minimal initialization time, so you can spin up tiny services or command-line tools almost instantly.

- **Community extensions**  
  A wealth of forks and plugins add features like quantization recipes, GPU kernels, chat UIs, etc.


### What happens if you don’t use llama.cpp?

- You’d have to write your own loader to read `consolidated.00.pth` and apply `params.json`.  
- You’d need a heavy framework (PyTorch/TF) and GPU drivers to run efficiently.  
- You’d miss out on the GGML quantization and CPU optimizations.  
- You’d have to handle tokenization yourself (though Hugging Face’s `transformers` can help).  
- Your deployment would be bulkier, slower to start, and harder to port to non-Python environments.


### Getting Started with llama.cpp

```bash
  # Clone the repo
  git clone https://github.com/ggerganov/llama.cpp
  cd llama.cpp
  
  # Build llama.cpp
  mkdir -p build && cd build
  cmake .. -DLLAMA_BUILD_STATIC=ON -DCMAKE_BUILD_TYPE=Release
  cmake --build . --parallel
  
  pip install -r requirement.txt
```
