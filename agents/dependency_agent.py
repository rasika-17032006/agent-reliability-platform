import sys
import os
from pathlib import Path
import requests as http_req

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from core_platform.model_client import call_llm

class DependencyAgent:
    def __init__(self):
        pass

    def run(self, repo_path: str, mode: str = "automatic") -> dict:
        print("[DependencyAgent] Reading repo and calling local AI...")
        repo = Path(repo_path)
        
        # Check for requirements.txt file
        req_file = repo / "requirements.txt"
        if not req_file.exists():
            return {
                "status": "SKIPPED", 
                "step_name": "Dependency Agent Analysis Skipped",
                "reason": "No requirements.txt found in the repository root directory.",
                "confidence": 1.0,
                "verdict": True
            }

        requirements = req_file.read_text()
        outdated = []
        
        # Find outdated packages using public PyPI JSON APIs
        for line in requirements.splitlines():
            line = line.strip()
            if "==" not in line or line.startswith("#"):
                continue
            try:
                pkg, pinned = line.split("==", 1)
                pkg = pkg.strip()
                pinned = pinned.strip()
                resp = http_req.get(f"https://pypi.org/pypi/{pkg}/json", timeout=8)
                if resp.status_code == 200:
                    latest = resp.json()["info"]["version"]
                    if latest != pinned:
                        outdated.append({
                            "package": pkg,
                            "pinned": pinned,
                            "latest": latest
                        })
            except Exception:
                continue

        # Look up package references inside python codebase files
        usages = {}
        for py_file in repo.rglob("*.py"):
            try:
                content = py_file.read_text(errors="ignore")
                rel = str(py_file.relative_to(repo))
                for pkg_info in outdated:
                    pkg = pkg_info["package"]
                    if pkg.lower() in content.lower():
                        usages.setdefault(pkg, []).append(rel)
            except Exception:
                continue

        # Build structural summary data strings
        outdated_text = "\n".join(
            f"  - {p['package']}: {p['pinned']} → {p['latest']}" for p in outdated
        ) or "  None detected"
        
        usage_text = "\n".join(
            f"  {pkg}: used in {', '.join(files)}" for pkg, files in usages.items()
        ) or "  No usage found in .py files"

        # Construct prompt structure for Ollama model ingestion
        prompt = f"""You are a senior Python engineer doing a dependency audit.
requirements.txt contents:
{requirements}

Outdated packages found (current → latest):
{outdated_text}

Where each package is used in the codebase:
{usage_text}

Your tasks:
1. List each outdated package and assess upgrade risk (LOW/MEDIUM/HIGH).
2. For HIGH risk packages, explain what breaking changes to watch for.
3. Recommend which to upgrade immediately and which need careful testing.
4. Write the exact updated requirements.txt lines.

Be specific and actionable. Reference the actual packages and versions above."""

        ai_response = call_llm(prompt)

        # Handle explicit manual failure conditions if selected
        if mode == "manual_error" or len(outdated) > 5:
            return {
                "status": "FAILED",
                "step_name": "Dependency Agent Analysis Failed",
                "reason": f"VULNERABILITY WARNING: Found {len(outdated)} outdated external modules.",
                "confidence": 0.95,
                "verdict": False,
                "ai_analysis": ai_response
            }

        return {
            "status": "COMPLETED",
            "step_name": "Dependency Agent Analysis Completed",
            "reason": f"Scanned dependency map successfully. Outdated items flagged: {len(outdated)}.",
            "confidence": 0.95,
            "verdict": True,
            "ai_analysis": ai_response
        }