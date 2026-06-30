# import sys
# import os
# import subprocess
# from pathlib import Path

# # Add the project root directory to sys.path so it can find core_platform modules
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from core_platform.model_client import call_llm

# class TestTriageAgent:
#     def __init__(self):
#         pass

#     def run(self, repo_path: str, mode: str = "automatic") -> dict:
#         print("[TestTriageAgent] Running tests and calling local AI...")
#         repo = Path(repo_path)
        
#         # Look for typical test files inside the target codebase repository
#         test_files = list(repo.rglob("test_*.py")) + list(repo.rglob("*_test.py"))
#         if not test_files:
#             return {
#                 "status": "SKIPPED", 
#                 "step_name": "Test Triage Agent Analysis Skipped",
#                 "reason": "No valid unit test files found inside the repository space.",
#                 "confidence": 1.0,
#                 "verdict": True
#             }

#         run_outputs = []
#         # Run tests 3 times consecutively to check for potential test flakiness
#         for i in range(3):
#             result = subprocess.run(
#                 ["python", "-m", "pytest", "-v", "--tb=short", "-q", "--no-header"],
#                 cwd=repo,
#                 capture_output=True, text=True, timeout=60,
#                 env={**os.environ, "PYTHONPATH": str(repo)}
#             )
#             run_outputs.append({
#                 "run": i + 1,
#                 "passed": result.returncode == 0,
#                 "output": (result.stdout[-800:] + result.stderr[-200:]) if (result.stdout or result.stderr) else "No output"
#             })

#         # Track failure instances across our run passes
#         fail_in_runs = {}
#         for r in run_outputs:
#             for line in r["output"].splitlines():
#                 if "FAILED" in line and "::" in line:
#                     name = line.split("FAILED")[-1].strip()
#                     fail_in_runs.setdefault(name, []).append(r["run"])

#         flaky = [t for t, runs in fail_in_runs.items() if 0 < len(runs) < len(run_outputs)]
#         always_failing = [t for t, runs in fail_in_runs.items() if len(runs) == len(run_outputs)]

#         # Read contents of test files to provide deep inspection context to Ollama
#         test_source = ""
#         for tf in test_files[:5]:
#             try:
#                 test_source += f"\n=== {tf.name} ===\n{tf.read_text(errors='ignore')[:1000]}\n"
#             except Exception:
#                 continue

#         run_summary = "\n".join(f"  Run {r['run']}: {'PASS' if r['passed'] else 'FAIL'}" for r in run_outputs)
        
#         prompt = f"""You are a senior QA engineer diagnosing test failures.
# Test run results (3 attempts):
# {run_summary}

# Always failing tests:
# {chr(10).join(always_failing) or "  None"}

# Flaky tests (sometimes pass, sometimes fail):
# {chr(10).join(flaky) or "  None"}

# Last run raw output snippet:
# {run_outputs[-1]['output']}

# Test source code context:
# {test_source[:2500]}

# Your tasks:
# 1. Identify the specific ROOT CAUSE for each failing or flaky test if visible.
# 2. Suggest concrete structural adjustments or fixing scripts to fix it.
# 3. Classify whether it's minor or deployment-blocking.

# Be concise and highly actionable."""

#         ai_response = call_llm(prompt)
#         total_failed = len(always_failing) + len(flaky)

#         if mode == "manual_error" or total_failed > 0:
#             return {
#                 "status": "FAILED",
#                 "step_name": "Test Triage Agent Analysis Failed",
#                 "reason": f"TEST FAILURE DETECTED: Found {total_failed} failing test assertions.",
#                 "confidence": 0.90,
#                 "verdict": False,
#                 "ai_analysis": ai_response
#             }

#         return {
#             "status": "COMPLETED",
#             "step_name": "Test Triage Agent Analysis Completed",
#             "reason": "All discovered unit test paths passed execution cleanly.",
#             "confidence": 0.88,
#             "verdict": True,
#             "ai_analysis": ai_response
#         }












import sys
import os
import subprocess
from pathlib import Path

# Add the project root directory to sys.path so it can find core_platform modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core_platform.model_client import call_llm

class TestTriageAgent:
    def __init__(self):
        pass

    def run(self, repo_path: str, mode: str = "automatic") -> dict:
        print("[TestTriageAgent] Running tests and calling local AI...")
        repo = Path(repo_path)
        
        # Look for typical test files inside the target codebase repository
        test_files = list(repo.rglob("test_*.py")) + list(repo.rglob("*_test.py"))
        if not test_files:
            return {
                "status": "SKIPPED", 
                "step_name": "Test Triage Agent Analysis Skipped",
                "reason": "No valid unit test files found inside the repository space.",
                "confidence": 1.0,
                "verdict": True,
                "failed_tests": 0
            }

        run_outputs = []
        # Run tests 3 times consecutively to check for potential test flakiness
        for i in range(3):
            # FIXED: Forcing sys.executable ensures it locks onto your current active (venv)
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "-v", "--tb=short", "-q", "--no-header"],
                cwd=repo,
                capture_output=True, text=True, timeout=60,
                env={**os.environ, "PYTHONPATH": str(repo)}
            )
            
            # FIXED: Defensive guard catching environment missing module errors
            combined_error_stream = (result.stdout or "") + (result.stderr or "")
            if "No module named pytest" in combined_error_stream:
                return {
                    "status": "FAILED",
                    "step_name": "Test Triage Infrastructure Error",
                    "reason": "CRITICAL CONFIGURATION ERROR: Pytest is not installed in the target interpreter path.",
                    "confidence": 0.0,
                    "verdict": False,
                    "failed_tests": 1,
                    "ai_analysis": "The automation framework completely failed to initialize unit tests because python cannot find the 'pytest' package module."
                }

            run_outputs.append({
                "run": i + 1,
                "passed": result.returncode == 0,
                "output": (result.stdout[-800:] + result.stderr[-200:]) if combined_error_stream else "No output"
            })

        # Track failure instances across our run passes
        fail_in_runs = {}
        for r in run_outputs:
            for line in r["output"].splitlines():
                if "FAILED" in line and "::" in line:
                    name = line.split("FAILED")[-1].strip()
                    fail_in_runs.setdefault(name, []).append(r["run"])

        flaky = [t for t, runs in fail_in_runs.items() if 0 < len(runs) < len(run_outputs)]
        always_failing = [t for t, runs in fail_in_runs.items() if len(runs) == len(run_outputs)]

        # Read contents of test files to provide deep inspection context to Ollama
        test_source = ""
        for tf in test_files[:5]:
            try:
                test_source += f"\n=== {tf.name} ===\n{tf.read_text(errors='ignore')[:1000]}\n"
            except Exception:
                continue

        run_summary = "\n".join(f"  Run {r['run']}: {'PASS' if r['passed'] else 'FAIL'}" for r in run_outputs)
        
        prompt = f"""You are a senior QA engineer diagnosing test failures.
Test run results (3 attempts):
{run_summary}

Always failing tests:
{chr(10).join(always_failing) or "  None"}

Flaky tests (sometimes pass, sometimes fail):
{chr(10).join(flaky) or "  None"}

Last run raw output snippet:
{run_outputs[-1]['output']}

Test source code context:
{test_source[:2500]}

Your tasks:
1. Identify the specific ROOT CAUSE for each failing or flaky test if visible.
2. Suggest concrete structural adjustments or fixing scripts to fix it.
3. Classify whether it's minor or deployment-blocking.

Be concise and highly actionable."""

        ai_response = call_llm(prompt)
        total_failed = len(always_failing) + len(flaky)

        if mode == "manual_error" or total_failed > 0:
            return {
                "status": "FAILED",
                "step_name": "Test Triage Agent Analysis Failed",
                "reason": f"TEST FAILURE DETECTED: Found {total_failed} failing test assertions.",
                "confidence": 0.90,
                "verdict": False,
                "ai_analysis": ai_response,
                "failed_tests": total_failed  # FIXED: Required for orchestrator dynamic tracking metrics
            }

        return {
            "status": "COMPLETED",
            "step_name": "Test Triage Agent Analysis Completed",
            "reason": "All discovered unit test paths passed execution cleanly.",
            "confidence": 0.88,
            "verdict": True,
            "ai_analysis": ai_response,
            "failed_tests": 0  # FIXED: Required for orchestrator dynamic tracking metrics
        }
