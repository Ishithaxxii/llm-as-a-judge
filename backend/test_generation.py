import json
import urllib.request
import urllib.error
from pathlib import Path

# Load API keys from backend/.env. Never print or commit this file.
env = {}
for line in Path(".env").read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip().strip('"').strip("'")

PROMPT = "In one sentence, explain what an LLM evaluator does."


def post_json(url: str, headers: dict, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            **headers,
            "Content-Type": "application/json",
            "User-Agent": "LLMAJ/1.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=40) as response:
        return json.loads(response.read().decode("utf-8"))


def test_gemini() -> None:
    print("\n--- GEMINI TEST ---")
    try:
        api_key = env["GEMINI_API_KEY"]
        result = post_json(
            "https://generativelanguage.googleapis.com/v1beta/"
            "models/gemini-3.5-flash:generateContent?key=" + api_key,
            {},
            {"contents": [{"parts": [{"text": PROMPT}]}]},
        )
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        print(text)
        print("Gemini generation: SUCCESS")
    except urllib.error.HTTPError as exc:
        print(f"Gemini HTTP error: {exc.code}")
        print("Details:", exc.read().decode("utf-8", errors="replace")[:1000])
    except (KeyError, ValueError, OSError) as exc:
        print(f"Gemini generation: FAILED: {type(exc).__name__}: {exc}")


def test_groq() -> None:
    print("\n--- GROQ TEST ---")
    try:
        api_key = env["GROQ_API_KEY"]
        result = post_json(
            "https://api.groq.com/openai/v1/chat/completions",
            {"Authorization": "Bearer " + api_key},
            {
                "model": "openai/gpt-oss-20b",
                "messages": [{"role": "user", "content": PROMPT}],
                "max_completion_tokens": 150,
            },
        )
        print(result["choices"][0]["message"]["content"])
        print("Groq generation: SUCCESS")
    except urllib.error.HTTPError as exc:
        print(f"Groq HTTP error: {exc.code}")
        print("Details:", exc.read().decode("utf-8", errors="replace")[:1000])
    except (KeyError, ValueError, OSError) as exc:
        print(f"Groq generation: FAILED: {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    if not Path(".env").exists():
        raise SystemExit(
            "Missing backend/.env. Create it with GEMINI_API_KEY and GROQ_API_KEY."
        )
    test_gemini()
    test_groq()
