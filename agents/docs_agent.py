import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core_platform.model_client import call_llm

class DocsAgent:
    def __init__(self):
        pass

    def run(self, repo_path: str, mode: str = "automatic") -> dict:
        print("[DocsAgent] Scanning codebase for documentation generation...")
        repo = Path(repo_path)
        
        py_files = [
            f for f in repo.rglob("*.py")
            if "__pycache__" not in str(f) and "venv" not in str(f)
        ]
        
        if not py_files:
            return {
                "status": "SKIPPED",
                "step_name": "Documentation Agent Analysis Skipped",
                "reason": "No Python files found to document.",
                "confidence": 1.0,
                "verdict": True
            }

        code_context = ""
        for f in py_files[:5]:
            try:
                code_context += f"\n=== {f.name} ===\n{f.read_text(errors='ignore')[:800]}\n"
            except Exception:
                continue

        prompt = f"""You are a technical writer. Generate a concise README markdown documentation structure for this repository based on the following files:

{code_context}

Provide a clear project overview, architecture details, and usage summary."""

        ai_response = call_llm(prompt)
        
        if mode == "manual_error":
            return {
                "status": "FAILED",
                "step_name": "Documentation Agent Analysis Failed",
                "reason": "Forced manual operational failure path.",
                "confidence": 0.5,
                "verdict": False,
                "ai_analysis": ai_response
            }

        return {
            "status": "COMPLETED",
            "step_name": "Documentation Agent Analysis Completed",
            "reason": f"Generated documentation structure covering {len(py_files[:5])} module components.",
            "confidence": 0.95,
            "verdict": True,
            "ai_analysis": ai_response
        }