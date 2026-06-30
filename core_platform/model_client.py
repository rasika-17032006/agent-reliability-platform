import os
import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:1.5b")

def call_llm(prompt: str) -> str:
    """Call local Ollama — free, no API key, works offline."""
    print(f"[LLM] Calling {OLLAMA_MODEL} via Ollama...")
    try:
        resp = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.1, "num_predict": 2000},
            },
            timeout=300
        )
        resp.raise_for_status()
        result = resp.json().get("response", "").strip()
        print(f"[LLM] Response received ({len(result)} chars)")
        return result
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "[LLM] Ollama not running. Run: ollama serve"
        )
    except Exception as e:
        raise RuntimeError(f"[LLM] Call failed: {e}")