from transformers import pipeline
from huggingface_hub import snapshot_download

print("Running transformers basics...")

# Option 1: Path to your local model downloades from Hugging Face
model_path = "/Users/pedrorodriguezdeledesmajimenez/scripts/llm_models/gemma-3-270m/"

# Option 2: Download from Hugging Face hub
# file_path = snapshot_download(repo_id="google/gemma-3-270m")
# print(file_path)

# Option 3: Load directly from Hugging Face hub
# model_path = "google/gemma-3-270m"  # HF repo ID


# RUN
model = pipeline("text-generation",
                 model=model_path,
                 device=0) # Use device=0 for GPU, device=-1 for CPU

print("Model loaded successfully. Genererating response...")

response = model("Hi")
print(response[0]['generated_text'])
