# Running a Model with Hugging Face Transformers
This guide will help you run large language models using the Hugging Face Transformers library, which is a popular alternative to `llama.cpp`. It supports a wide range of models and provides a Pythonic interface for easy integration.
---



## 1. Load a Model in Python

Here’s an example using **Llama 3 8B Instruct** from Hugging Face:

```python
    from transformers import pipeline
    from huggingface_hub import snapshot_download

    # Option 1: Path to your local model downloades from Hugging Face
    model_path = "/Users/pedrorodriguezdeledesmajimenez/scripts/llm_models/gemma-3-270m/"
    
    # Option 2: Download from Hugging Face hub
    # file_path = snapshot_download(repo_id="google/gemma-3-270m")
    # print(file_path)
    
    # Option 3: Load directly from Hugging Face hub
    # model_path = "google/gemma-3-270m"  # HF repo ID
```
## 2. Text Generation Example

```python
    model = pipeline("text-generation",
                     model=model_path,
                     device=0) # Use device=0 for GPU, device=-1 for CPU
    
    print("Model loaded successfully. Genererating response...")
    
    response = model("Hi")
    print(response[0]['generated_text'])
```

## 3. Run from the CLI (Optional)

You can also use **`transformers-cli`** to quickly test:

```bash
transformers-cli env
```


---

## ✅ Key Differences from llama.cpp

| Feature      | llama.cpp                          | Transformers                                   |
| ------------ | ---------------------------------- | ---------------------------------------------- |
| Model format | GGUF only                          | HF format (Safetensors, PyTorch)               |
| Performance  | Very fast on CPU, Metal, CUDA      | Best on GPU (with CUDA, ROCm)                  |
| Quantization | Built-in (Q2-Q8)                   | Limited, needs extra tools like `bitsandbytes` |
| Ease of use  | CLI-friendly, minimal dependencies | Full-featured Python ecosystem                 |
