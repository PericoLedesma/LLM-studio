## Downloaded Model Files --> raw PyTorch checkpoint
When you download or export a Llama 3 model from Meta or Hugging Face, you typically get:
```bash
Llama3.2-1B/
├── checklist.chk           # Optional integrity check file
├── consolidated.00.pth     # Raw PyTorch weight shards
├── params.json             # Model architecture and hyperparameters
└── tokenizer.model         # SentencePiece tokenizer
```

## What is GGUF?

**GGUF** (GGML Universal Format) is a self-contained binary format used in the `llama.cpp` ecosystem. It packages:

1. **Model architecture parameters** (e.g., hidden size, layer count)  
2. **Tokenizer data** (e.g., vocabulary, merges, or token-to-string mappings)  
3. **Weight tensors** (optionally quantized), along with quantization metadata  

This unified format supports fast loading, CPU-based inference, and streamlined quantization workflows.

---

## Common Model Formats

Many local LLMs are shared via platforms like **Hugging Face**, originally focused on Transformer-based models (e.g. BERT, GPT) and now hosting a broad range of architectures.

### 1. **PyTorch (`.pt`)**

Native to the PyTorch framework, these models are often labeled with precision tags like `fp16` or `fp32`. They represent the original, full-fidelity versions of Transformer-based models. While accurate, they require significant GPU memory and are best suited for high-end hardware.

### 2. **GGML / GGUF**

- **GGML** (Georgi Gerganov Machine Learning) allows LLM inference on CPU (and optionally GPU) with aggressive quantization to reduce size and memory usage.  
- **GGUF** is the modern successor to GGML, designed to be extensible and fully supported in the latest versions of `llama.cpp`.

### 3. **GPTQ**

A GPU-friendly quantized format, typically distributed as `.safetensors` files. GPTQ models are commonly 4-bit (sometimes 3-bit), offering fast inference speeds with low memory use — ideal for running large models entirely on GPU.

---

### Choosing the Right Format

| Format     | Best For                        | Key Tools                      |
|------------|----------------------------------|--------------------------------|
| **PyTorch**| High-fidelity training/fine-tuning | `transformers`                |
| **GGUF**   | CPU inference, easy quantization | `llama.cpp`                   |
| **GPTQ**   | Fast GPU inference               | AutoGPTQ, ExLlama, GPTQ-for-LLaMa |

> **Note:** Other formats like ONNX exist, but PyTorch, GGUF, and GPTQ are the most widely used in local LLM deployment.

---

### GPTQ Runtime Options

For running **GPTQ models**, popular tools include:

- [`GPTQ-for-LLaMa`](https://github.com/qwopqwop200/GPTQ-for-LLaMa)  
- [`AutoGPTQ`](https://github.com/PanQiWei/AutoGPTQ)  
- [`ExLlama`](https://github.com/turboderp/exllama) / [`ExLlama-HF`](https://github.com/huggingface/transformers/pull/24906)