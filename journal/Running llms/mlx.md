
# MLX / mlx-lm

MLX is Apple's open-source machine learning framework built specifically for Apple Silicon (M1–M4). Unlike llama.cpp or Transformers, MLX runs computations directly on the unified memory architecture of M-series chips, making it 2–3x faster than llama.cpp on the same hardware.

It is currently the best option for local inference if you are on a Mac.

---

## How It Works

MLX treats CPU and GPU memory as a single unified pool, eliminating the data transfers that slow down other frameworks on Apple Silicon. The `mlx-lm` package is the high-level wrapper for running LLMs with MLX.

---

## Install

```bash
pip install mlx-lm
```

Requires macOS 13.5+ and an Apple Silicon Mac. Does not work on Intel Macs.

---

## Finding Models

Models must be in MLX format (weights stored as `.safetensors` with MLX-specific quantization). A large and growing collection is available directly on HuggingFace under the `mlx-community` organization:

```
https://huggingface.co/mlx-community
```

Examples:
- `mlx-community/Llama-3.2-3B-Instruct-4bit`
- `mlx-community/Mistral-7B-Instruct-v0.3-4bit`
- `mlx-community/Qwen2.5-7B-Instruct-4bit`

---

## Basic Usage

### Command line
```bash
mlx_lm.generate --model mlx-community/Llama-3.2-3B-Instruct-4bit --prompt "Explain transformers in one sentence"
```

### Python
```python
from mlx_lm import load, generate

model, tokenizer = load("mlx-community/Llama-3.2-3B-Instruct-4bit")

response = generate(model, tokenizer, prompt="Explain transformers in one sentence", verbose=True)
print(response)
```

### Chat format
```python
from mlx_lm import load, generate

model, tokenizer = load("mlx-community/Llama-3.2-3B-Instruct-4bit")

messages = [{"role": "user", "content": "What is the capital of France?"}]
prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

response = generate(model, tokenizer, prompt=prompt, max_tokens=256)
print(response)
```

---

## Key Parameters for `generate()`

| Parameter | Description |
|-----------|-------------|
| `max_tokens` | Maximum tokens to generate (default: 256) |
| `temp` | Sampling temperature — 0.0 for greedy, higher for more random |
| `verbose` | Print tokens as they stream |

---

## MLX vs. Other Local Inference Options (on Mac)

| Tool | Speed on Apple Silicon | Setup complexity |
|------|----------------------|-----------------|
| **MLX** | Fastest | Low |
| **llama.cpp** | Fast | Low |
| **Ollama** | Fast (uses llama.cpp under the hood) | Very low |
| **Transformers** | Slow (not Metal-optimized for LLMs) | Medium |

Use **MLX** when you want maximum performance on Mac.  
Use **Ollama** when you want the simplest setup and don't need peak speed.  
Use **llama.cpp** when you need fine-grained control over the runtime.
