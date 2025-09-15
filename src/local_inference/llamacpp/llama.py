from llama_cpp import Llama

# Load a GGUF model
llm = Llama(model_path="/Users/pedrorodriguezdeledesmajimenez/scripts/llm_models/mistral-7b-instruct-v0.2.Q4_K_M.gguf")

# Run inference
output = llm("Write a haiku about Python", max_tokens=64)
print(output["choices"][0]["text"])