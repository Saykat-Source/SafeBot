import requests
import os

# For OpenAI integration (if you want to use it)
try:
    import openai
except ImportError:
    openai = None

# Query Gemma:2b via Ollama (local)
def query_gemma(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "gemma:2b",
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json().get("response", "")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error connecting to Ollama: {e}"

# Query OpenAI (online) - compatible with openai>=1.0.0
def query_openai(prompt):
    if openai is None:
        return "OpenAI module not installed."
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "OpenAI API key not set in environment variables."
    client = openai.OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4"
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to OpenAI: {e}"

# Unified interface
def query_llm(prompt, model="gemma"):
    if model == "gemma":
        return query_gemma(prompt)
    elif model == "openai":
        return query_openai(prompt)
    else:
        return "Invalid model selected."
