from huggingface_hub import InferenceClient
import os


client = InferenceClient(
    api_key=os.environ.get("HUGGINGFACEHUB_API_TOKEN"),
    provider="auto",   # Automatically selects best provider
)

# Chat completion
completion = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V3-0324",
    messages=[{"role": "user", "content": "A story about hiking in the mountains"}]
)

print(completion)
