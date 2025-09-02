# 🧩 How LLM Components Fit Together

When working with LLMs, there are several layers in the stack:

---

## 1. Frameworks (Training & Base)
| Layer          | Examples                 | Role                                                                                                                                |
|----------------|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| **Frameworks** | PyTorch, TensorFlow, JAX | Core libraries used to **train models** and run computations on CPU/GPU/TPU. Models are created and trained using these frameworks. |

---

## 2. Model Files (Trained Weights)
| Layer           | Examples                                              | Role                                                                                                                                   |
|-----------------|-------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| **Model files** | `.pt`, `.bin`, `.safetensors`, `.gguf`, `.ggml`, ONNX | These are **serialized trained models**. Some formats are for training (`.pt`), others are optimized for **inference** (`GGUF`, ONNX). |

---

## 3. Inference Libraries
| Layer         | Examples                                              | Role                                                                                                                               |
|---------------|-------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| **Libraries** | Transformers, HuggingFace_hub, CTransformers, mlc-llm | Load models from disk or API, run inference locally or in the cloud. Can also handle model conversion (e.g., PyTorch → GGUF/ONNX). |

---

## 4. SDKs (Online Inference)
| Layer    | Examples                                | Role                                                                                                                                  |
|----------|-----------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| **SDKs** | OpenAI, Cohere, Azure OpenAI, Anthropic | Provide **simplified access to online APIs**. Handle authentication, networking, and model invocation. Typically **vendor-specific**. |

---

## 5. Orchestration & Chains
| Layer             | Examples                         | Role                                                                                                                        |
|-------------------|----------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| **Orchestration** | LangChain, Llama-Index, Haystack | Build pipelines and chains that connect models (local or online) with prompts, memory, and external data (RAG, embeddings). |

---

### 🔹 How it all connects
1. **Frameworks** → Used to train models → produce **model files**.  
2. **Model files** → Can be loaded by **inference libraries** (Transformers, CTransformers) for local usage.  
3. **SDKs** → Access models hosted online without needing to handle the training or framework directly.  
4. **Orchestration libraries** → Connect multiple models, local or online, into workflows or agents.  

---

### 📌 Example Workflow
- Train a model with **PyTorch** → save as `.pt`  
- Convert `.pt` → `.gguf` → run locally with **CTransformers**  
- Or use the same prompt with **OpenAI SDK** for online inference  
- Use **LangChain** to create a chain combining local and online models with prompt templates  

---

✅ **Key Takeaway:**  
- Frameworks = **training / building models**  
- Model files = **trained weights**  
- Libraries = **run models locally**  
- SDKs = **run models online**  
- Orchestration = **connect models and workflows**  