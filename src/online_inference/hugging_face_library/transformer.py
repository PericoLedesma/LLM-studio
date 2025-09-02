from transformers import AutoModelForCausalLM

# 1. Load a model
# Load model directly
model = AutoModelForCausalLM.from_pretrained("apple/FastVLM-0.5B", trust_remote_code=True, torch_dtype="auto")

# 2. Generate text
prompt = "Explain the difference between supervised and unsupervised learning in simple terms."

output = model(prompt, max_new_tokens=100)
print(output)