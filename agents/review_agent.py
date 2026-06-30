# import sys
# import os
# import subprocess
# from pathlib import Path

# # Add the project root directory to sys.path so it can find core_platform modules
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from core_platform.model_client import call_llm

# class ReviewAgent:
#     def __init__(self):
#         pass

#     def run(self, repo_path: str, mode: str = "automatic") -> dict:
#         print("[ReviewAgent] Reading codebase and calling local AI...")
#         repo = Path(repo_path)
        
#         # Read Python source files while ignoring environments or temporary folders
#         py_files = [
#             f for f in repo.rglob("*.py")
#             if "test_" not in f.name
#             and "__pycache__" not in str(f)
#             and "venv" not in str(f)
#         ]
        
#         if not py_files:
#             return {
#                 "status": "SKIPPED",
#                 "step_name": "Review Agent Analysis Skipped",
#                 "reason": "No main Python application files detected to review.",
#                 "confidence": 1.0,
#                 "verdict": True
#             }

#         code_context = ""
#         for f in py_files[:8]:  # Limit to the first 8 files to respect model context
#             try:
#                 content = f.read_text(errors="ignore")
#                 rel = str(f.relative_to(repo))
#                 code_context += f"\n=== {rel} ===\n{content[:800]}\n"
#             except Exception:
#                 continue

#         # Run external linting/security scanners if available
#         ruff_out = self._run_tool(["python", "-m", "ruff", "check", str(repo), "--output-format=text"], repo)
#         bandit_out = self._run_tool(["python", "-m", "bandit", "-r", str(repo), "-f", "text", "-q"], repo)

#         prompt = f"""You are a strict senior code reviewer. Review this codebase thoroughly.

# Source code context:
# {code_context}

# Static analysis — Ruff (style/lint):
# {ruff_out}

# Static analysis — Bandit (security):
# {bandit_out}

# Your tasks:
# 1. List all code quality issues found (missing checks, naming bugs, missing error handling).
# 2. For each issue, provide the filename and the recommended structural fix.
# 3. Provide an overall verdict: APPROVE or REQUEST_CHANGES.

# Be precise, highly critical, and professional."""

#         ai_response = call_llm(prompt)

#         # Parse verdict from response string
#         verdict = True
#         status = "COMPLETED"
#         step_name = "Review Agent Analysis Completed"
#         reason_msg = "Structural code review completed successfully with no critical blockers."

#         if "REQUEST_CHANGES" in ai_response.upper() or mode == "manual_error":
#             verdict = False
#             status = "FAILED"
#             step_name = "Review Agent Analysis Failed"
#             reason_msg = "Code review highlighted patterns requiring structural changes."

#         return {
#             "status": status,
#             "step_name": step_name,
#             "reason": reason_msg,
#             "confidence": 0.90,
#             "verdict": verdict,
#             "ai_analysis": ai_response
#         }

#     def _run_tool(self, cmd: list, cwd: Path) -> str:
#         try:
#             r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=20)
#             return (r.stdout or r.stderr)[:1000] or "No issues found"
#         except FileNotFoundError:
#             return f"Tool execution omitted (command not installed: {cmd[2]})"
#         except Exception as e:
#             return f"Tool diagnostic error: {e}"


















import sys
import os
import subprocess
from pathlib import Path

# Add the project root directory to sys.path so it can find core_platform modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core_platform.model_client import call_llm

class ReviewAgent:
    def __init__(self):
        pass

    def run(self, repo_path: str, mode: str = "automatic") -> dict:
        print("[ReviewAgent] Reading codebase and calling local AI...")
        repo = Path(repo_path)
        
        # Read Python source files while ignoring environments or temporary folders
        py_files = [
            f for f in repo.rglob("*.py")
            if "test_" not in f.name
            and "__pycache__" not in str(f)
            and "venv" not in str(f)
        ]
        
        if not py_files:
            return {
                "status": "SKIPPED",
                "step_name": "Review Agent Analysis Skipped",
                "reason": "No main Python application files detected to review.",
                "confidence": 1.0,
                "verdict": True
            }

        code_context = ""
        for f in py_files[:8]:  # Limit to the first 8 files to respect model context
            try:
                content = f.read_text(errors="ignore")
                rel = str(f.relative_to(repo))
                code_context += f"\n=== {rel} ===\n{content[:800]}\n"
            except Exception:
                continue

        # FIXED: Enforced sys.executable containment matrix with clean, modern CLI flags to prevent syntax mismatches
        ruff_out = self._run_tool([sys.executable, "-m", "ruff", "check", str(repo), "--output-format", "pylint"], repo)
        bandit_out = self._run_tool([sys.executable, "-m", "bandit", "-r", "-f", "txt", "-q", str(repo)], repo)

        prompt = f"""You are a strict senior code reviewer. Review this codebase thoroughly.

Source code context:
{code_context}

Static analysis — Ruff (style/lint):
{ruff_out}

Static analysis — Bandit (security):
{bandit_out}

Your tasks:
1. List all code quality issues found (missing checks, naming bugs, missing error handling).
2. For each issue, provide the filename and the recommended structural fix.
3. Provide an overall verdict: APPROVE or REQUEST_CHANGES.

Be precise, highly critical, and professional."""

        ai_response = call_llm(prompt)

        # Parse verdict from response string
        verdict = True
        status = "COMPLETED"
        step_name = "Review Agent Analysis Completed"
        reason_msg = "Structural code review completed successfully with no critical blockers."

        if "REQUEST_CHANGES" in ai_response.upper() or mode == "manual_error":
            verdict = False
            status = "FAILED"
            step_name = "Review Agent Analysis Failed"
            reason_msg = "Code review highlighted patterns requiring structural changes."

        return {
            "status": status,
            "step_name": step_name,
            "reason": reason_msg,
            "confidence": 0.90,
            "verdict": verdict,
            "ai_analysis": ai_response
        }

    def _run_tool(self, cmd: list, cwd: Path) -> str:
        try:
            r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=20)
            combined_out = (r.stdout or "") + (r.stderr or "")
            
            # Defensive validation path capturing missing environment variables
            if "No module named" in combined_out:
                tool_name = cmd if len(cmd) > 2 else "scanner"
                return f"Tool execution runtime alert: {tool_name} package module missing inside active interpreter environment context."
                
            return combined_out[:1000] or "No issues found"
        except FileNotFoundError:
            tool_name = cmd if len(cmd) > 2 else "unknown_tool"
            return f"Tool execution omitted (command not installed: {tool_name})"
        except Exception as e:
            return f"Tool diagnostic error: {e}"
