
## Conversion Workflow
Below is a step-by-step guide to convert your raw PyTorch checkpoint into a single `.gguf` file using llama.cpp.

### 1. Prepare a Python Environment & Install Dependencies
```bash
python3 -m venv .venv          # Create a virtual environment
source .venv/bin/activate      # Activate it
pip install transformers[torch] tiktoken blobfile sentencepiece
```

### 2. Convert PyTorch Weights to Hugging Face Format
```bash
python \
  .venv/lib/python3.*/site-packages/transformers/models/llama/convert_llama_weights_to_hf.py \
  --input_dir   Llama3.2-1B/ \
  --model_size  1B \
  --llama_version 3 \
  --output_dir hf/
```
This produces an `hf/` directory with:
- `model-*.safetensors` (weights)
- `config.json` (HF config)
- Tokenizer files

### 3. Clone and Build llama.cpp
```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make
```
This builds the `convert-hf-to-gguf.py` and `llama-quantize` tools.

### 4. Convert Hugging Face Format to GGUF
```bash
./convert-hf-to-models_formats.md.py \
  ../hf/ \
  --outfile ../Llama3.2-1B.models_formats.md \
  --outtype f16
```
Result: a single `Llama3.2-1B.gguf` file ready for inference.

### 5. (Optional) Quantize Your GGUF
For smaller sizes or lower precision, use:
```bash
./llama-quantize \
  ../Llama3.2-1B.models_formats.md \
  ../Llama3.2-1B-q4_0.models_formats.md \
  Q4_0
```
Supported formats include `Q4_0`, `Q4_K_M`, `Q5_K_M`, `Q8_0`, etc.

## Running Inference with llama.cpp
```bash
./main \
  -m ../Llama3.2-1B.models_formats.md \
  -p "Hello, llama.cpp!"
```
This runs CPU-based inference without any heavy Python or GPU dependencies.
