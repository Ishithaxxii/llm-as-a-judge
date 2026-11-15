
import json
import urllib.request
import urllib.error
from pathlib import Path

# Read keys from .env without printing them.
env = {}
for line in Path(".env").read_text().splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip().strip('"').strip("'")

def check_provider(name, url, headers=None):
    print(f"\nChecking {name}...")
    request_headers = headers or {}
    request_headers["User-Agent"] = "LLMAJ/1.0"
    request = urllib.request.Request(url, headers=request_headers)

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            data = json.loads(response.read().decode())

        print(f"SUCCESS: {name} key is accepted.")

        if name == "Gemini":
            models = [
                item["name"].replace("models/", "")
                for item in data.get("models", [])
                if "generateContent" in item.get("supportedGenerationMethods", [])
            ]
        else:
            models = [
                item["id"]
                for item in data.get("data", [])
            ]

        print("Available models (first 10):")
        for model in models[:10]:
            print(" -", model)

    except urllib.error.HTTPError as e:
        print(f"HTTP ERROR: {e.code}")
        print(e.read().decode()[:500])
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")

gemini_key = env.get("GEMINI_API_KEY")
groq_key = env.get("GROQ_API_KEY")

if not gemini_key or not groq_key:
    print("Missing key. Check the names in backend/.env.")
else:
    check_provider(
        "Gemini",
        f"https://generativelanguage.googleapis.com/v1beta/models?key={gemini_key}"
    )

    check_provider(
        "Groq",
        "https://api.groq.com/openai/v1/models",
        {"Authorization": f"Bearer {groq_key}"}
    )