from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)


def query_ollama(prompt, model="llama3"):
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            text=True,
            capture_output=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"


@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    prompt = data.get("prompt", "")
    model = data.get("model", "llama3")
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    response = query_ollama(prompt, model)
    return jsonify({"response": response})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1000)