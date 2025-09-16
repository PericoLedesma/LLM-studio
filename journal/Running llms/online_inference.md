# 🌐 Online Inference Options for LLMs

Online inference allows you to run LLMs **remotely** without heavy local hardware.  
You send requests to a **model API**, and the server returns the generated output.  

---

### 1. How Online Inference Works

1. **Get API access**  
   - Sign up for a cloud provider (OpenAI, Hugging Face, Cohere, etc.) and obtain an API key.  

2. **Use a library/SDK (recommended)**  
   - Most providers offer official libraries to simplify API calls.  
   - Examples:  
     - `openai` → Python SDK for OpenAI API  
     - `huggingface_hub` → Hugging Face Inference Client  
     - `cohere` → Python SDK for Cohere API  

3. **Send a request**  
   - Provide:
     - **Prompt / input text**  
     - **Model name or version**  
     - Optional parameters (max tokens, temperature, top-p, etc.)  

4. **Receive a response**  
   - The library handles networking and authentication; you get model output directly in your code.  



### 2. Calling APIs

#### 🔹 OpenAI **SDK** 
```python
    from openai import OpenAI
    import os
    
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Write a short story"}]
    )
    print(response.choices[0].message.content)
```

#### 🔹 Hugging Face **library**
```python
    from huggingface_hub import InferenceClient
    import os
    
    client = InferenceClient(
        api_key=os.environ["HF_TOKEN"],
        provider="auto",   # Automatically selects best provider
    )
    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3-0324",
        messages=[{"role": "user", "content": "A story about hiking in the mountains"}]
    )
```

#### 🔹 Langchaing **library**
```python
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    
    # 1. Initialize the LLM (using OpenAI API under the hood)
    llm = ChatOpenAI(model="gpt-4o-mini")  # replace with your model of choice
    
    # 2. Create a simple prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("user", "{question}")
    ])
    
    # 3. Format the prompt with user input
    chain = prompt | llm  # Pipeline: prompt → model
    
    # 4. Run inference
    response = chain.invoke({"question": "What is the capital of Spain?"})
    
    print(response.content)
```

### 3. Raw HTTP vs SDKs

| Approach    | Pros                                 | Cons                               |
|-------------|--------------------------------------|------------------------------------|
| Raw HTTP    | Works everywhere, no extra libraries | More boilerplate (headers, auth).  |
| SDK/Library | Simpler, handles auth & parsing      | Must install provider-specific lib |


### ✅ Summary
•	Online inference = send input → cloud model → get output.  
•	Use libraries/SDKs (OpenAI, Hugging Face, Cohere) to simplify API calls.  
•	Choose a provider depending on model quality, cost, and scale.  
•	Best when local hardware is insufficient or you need always-updated models.  

---
# 📚 SDKs vs Libraries for Online Inference

When calling LLMs online, you can either use a **library** or an **SDK**.  
Both help you interact with APIs, but they serve slightly different purposes.  

## 🔹 Libraries
- **What they are**: General-purpose code packages that provide reusable functions or utilities.  
- **How they work**: Wrap around the API but often require you to handle details (auth, formatting, error handling).  
- **Examples**:
  - `transformers` → Can load local models or connect to Hugging Face Hub.  
  - `huggingface_hub` → Provides tools to query models, download weights, or call inference API.  
- **Best for**:
  - Flexibility (local + online).  
  - Research workflows.  
  - Developers who want more control. 

### 🔹 Libraries (General-Purpose / Multi-Provider)
| Library             | Maintainer / Ecosystem  | Notes                                                                                          |
|---------------------|-------------------------|------------------------------------------------------------------------------------------------|
| **transformers**    | Hugging Face            | Can load models locally or call Hugging Face Hub.                                              |
| **huggingface_hub** | Hugging Face            | Library to query/download models, also supports inference API.                                 |
| **langchain**       | Community (open-source) | Orchestration library; integrates multiple providers (OpenAI, HF, Cohere, etc.).               |
| **llama-index**     | Community (open-source) | Framework for building retrieval-augmented generation (RAG) pipelines; supports multiple APIs. |
| **Haystack**        | deepset                 | NLP framework; can integrate online APIs and local inference.                                  |
| **mlc-llm**         | MLC community           | Cross-platform runtime for LLMs, supports both local and remote inference.                     |
| **CTransformers**   | Community / GitHub      | Lightweight Python library for fast local inference with GGUF/GGML models; CPU & GPU support.  |

## 🔹 SDKs (Software Development Kits)
- **What they are**: Provider-specific toolkits designed to interact with a particular API.  
- **How they work**: Simplify API usage by handling **authentication, requests, and responses** internally.  
- **Examples**:
  - `openai` (Python/JS SDK for OpenAI API).  
  - `cohere` (SDK for Cohere API).  
  - `azure-ai` (Azure SDK for OpenAI on Azure).  
- **Best for**:
  - Production use (less boilerplate).  
  - Fast prototyping with a specific vendor.  
  - Easier error handling and updates (maintained by provider).  

### 🔹 SDKs (Provider-Specific)
| SDK                     | Provider / Platform            | Notes                                                                        |
|-------------------------|--------------------------------|------------------------------------------------------------------------------|
| **openai**              | OpenAI                         | Official Python/JS SDK, easy for GPT models (chat, embeddings, fine-tuning). |
| **cohere**              | Cohere                         | Python/JS SDK, text generation, embeddings, classification.                  |
| **azure-ai**            | Microsoft Azure                | SDK for Azure OpenAI Service (enterprise hosting of OpenAI models).          |
| **anthropic**           | Anthropic (Claude API)         | Official SDK for Claude models, optimized for chat use cases.                |
| **google-generativeai** | Google Cloud (Gemini/PaLM API) | SDK to interact with Gemini/PaLM via Vertex AI.                              |
| **ai21**                | AI21 Labs (Jurassic models)    | SDK for AI21’s LLMs, focused on text generation and editing.                 |


## ⚖️ Comparison Table

| Aspect          | Library                                    | SDK                                   |
|-----------------|--------------------------------------------|---------------------------------------|
| **Scope**       | General-purpose, may support local + cloud | Vendor-specific, focused on their API |
| **Ease of Use** | More setup (auth, formatting)              | Easier (built-in API helpers)         |
| **Flexibility** | Can work across multiple providers         | Tied to one provider                  |
| **Maintenance** | Community-driven (Hugging Face, etc.)      | Provider-maintained (OpenAI, Cohere)  |
| **Use Case**    | Research, experimentation                  | Production, vendor integration        |



## ✅ Summary
- **Libraries** → Broader, can be used for both local and online inference. More flexible but may need extra setup.  
- **SDKs** → Vendor-specific, easier for calling that provider’s API. Ideal for production and quick integration.  

