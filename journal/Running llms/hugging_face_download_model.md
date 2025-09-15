
# 📥 How to Download a Model from Hugging Face

Hugging Face hosts thousands of pre-trained models for NLP, computer vision, audio, and more.  
You can download them in several ways: using the **Transformers** library, the **huggingface_hub** client, or **Git**.

---
## 1️⃣ Using huggingface_hub CLI
 
```bash
    pip install huggingface_hub
    huggingface-cli login  # Authenticate with your Hugging Face account
    
    # Download a model
    huggingface-cli repo clone bert-base-uncased ./bert-base-uncased
    
    # or download specific files
    git clone https://huggingface.co/google/gemma-3-270m
```

```python
    from huggingface_hub import hf_hub_download
    
    file_path = hf_hub_download(repo_id="bert-base-uncased", filename="config.json")
    print(file_path)
```

## 2️⃣ Using Transformers (Recommended for NLP Models)

```bash
    pip install transformers
    from transformers import AutoModel, AutoTokenizer
    
    model_name = "bert-base-uncased"
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
```




