# import sys
# import os
# import json
# from pathlib import Path
# import ast

# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from core_platform.model_client import call_llm

# MAX_PROMPT_CHARS = 4000
# DEFAULT_CONSISTENCY_RUNS = 3  # Parallel execution threads for consensus verification


# class CodeDebuggerAgent:
#     def __init__(self, consistency_runs: int = DEFAULT_CONSISTENCY_RUNS):
#         self.consistency_runs = consistency_runs

#     def _verify_syntax_ast(self, file_path: Path, content: str) -> tuple[bool, str, bool]:
#         """
#         Deterministic syntax parser. Executes an authentic AST compilation trace 
#         for Python resources, or seamlessly routes other programming languages to 
#         the temperature-based semantic consensus matrix.
#         """
#         if file_path.suffix != ".py":
#             return (
#                 True,
#                 f"Static AST syntax verification bypassed — file extension '{file_path.suffix or 'none'}' "
#                 f"routed directly to multi-pass semantic consistency matrix.",
#                 False,
#             )
#         try:
#             ast.parse(content)
#             return True, "Parsed successfully with Python's ast module — no syntax errors.", True
#         except SyntaxError as e:
#             return False, f"ast.parse failed at line {e.lineno}, column {e.offset}: {e.msg}", True

#     def _ask_llm_once(self, content: str, extension: str, run_index: int) -> dict:
#         # Style variations simulate high-temperature semantic shifts inside the local model engine
#         analysis_modes = [
#             "Pass 1: Rigid Compiler Rule Check. Focus on standard layout and explicit compilation constraints.",
#             "Pass 2: Boundary Exception Check. Focus on data mutation logic and potential runtime errors.",
#             "Pass 3: Edge Case Verification. Focus on race conditions, types, and uncommon logical flow deadlocks."
#         ]
#         current_mode = analysis_modes[run_index if run_index < len(analysis_modes) else 1]

#         prompt = f"""You are an elite cross-compiler analysis engine inspecting source code strings for bugs, syntax errors, or logical faults.
# Target Language Framework/Extension Reference: {extension}
# Analysis Style Mode: {current_mode}

# ---
# {content[:MAX_PROMPT_CHARS]}
# ---

# CRITICAL INSTRUCTION: Analyze the text buffer carefully against standard compiler grammar and layout specifications for this language target.
# You must respond ONLY with a valid JSON object. Do not include markdown blocks, backticks, or trailing prose.

# The JSON structure must match this format precisely:
# {{
#     "has_errors": true or false,
#     "internal_certainty_score": 0.0 to 1.0,
#     "verdict_reason": "Clear one-sentence summary of the compilation status or major bug found",
#     "analysis_report": "Detailed architectural breakdown tracking detected anomalies, verified structural corrections, and technical causes"
# }}"""
#         raw = call_llm(prompt).strip()
#         if raw.startswith("```json"):
#             raw = raw[7:]
#         if raw.endswith("```"):
#             raw = raw[:-3]
#         return json.loads(raw.strip())

#     @staticmethod
#     def _result(status, reason, confidence, verdict, ai_analysis="", logs=None):
#         return {
#             "status": status,
#             "reason": reason,
#             "confidence": confidence,
#             "verdict": verdict,
#             "ai_analysis": ai_analysis,
#             "logs": logs or [],
#         }

#     def run(self, repo_path: str, mode: str = "automatic") -> dict:
#         file_path = Path(repo_path)

#         if not file_path.exists() or file_path.is_dir():
#             return self._result(
#                 "SKIPPED", "Target path does not exist or is a directory.", 1.0, True,
#                 logs=[
#                     "[Orchestrator] Task debug_code initiated.",
#                     "[CodeDebuggerAgent] Target path not found — skipping workspace execution branch.",
#                 ],
#             )

#         try:
#             content = file_path.read_text(encoding="utf-8", errors="ignore")
#         except Exception as e:
#             return self._result(
#                 "FAILED", f"Could not read file: {e}", 0.0, False,
#                 logs=[
#                     "[Orchestrator] Task debug_code initiated.",
#                     f"[CodeDebuggerAgent] System failure reading text buffer streams: {e}",
#                 ],
#             )

#         if not content.strip():
#             return self._result(
#                 "FAILED", "File is empty.", 0.0, False,
#                 logs=[
#                     "[Orchestrator] Task debug_code initiated.",
#                     f"[CodeDebuggerAgent] Content payload is empty for '{file_path.name}' — aborting verification.",
#                 ],
#             )

#         if mode == "manual_error":
#             return self._result(
#                 "FAILED", "Manual failure simulation active.", 1.0, False,
#                 ai_analysis="Simulated failure mode triggered for pipeline testing.",
#                 logs=[
#                     "[Orchestrator] Task debug_code initiated.",
#                     "[CodeDebuggerAgent] manual_error override active — forcing gate failure verdict.",
#                 ],
#             )

#         ast_passed, ast_message, ast_ran = self._verify_syntax_ast(file_path, content)
#         truncated = len(content) > MAX_PROMPT_CHARS

#         logs = [
#             "[Orchestrator] Task debug_code initiated.",
#             f"[AST Engine] {ast_message}",
#         ]

#         if ast_ran and not ast_passed:
#             logs.append("[Gate Input] proposed verdict=FAIL, confidence=1.00 (Deterministic baseline violation found).")
#             return self._result(
#                 "COMPLETED",
#                 f"AST compiler intercepted structural fault: {ast_message}",
#                 1.0,
#                 False,
#                 logs=logs,
#             )

#         reason, report = "", ""
#         error_votes = 0
#         critic_scores = []

#         try:
#             for i in range(self.consistency_runs):
#                 parsed = self._ask_llm_once(content, file_path.suffix or ".txt", run_index=i)
                
#                 has_error = bool(parsed.get("has_errors", False))
#                 critic_score = float(parsed.get("internal_certainty_score", 0.85))
                
#                 critic_scores.append(critic_score)
#                 if has_error:
#                     error_votes += 1
                    
#                 if i == 0:
#                     reason = parsed.get("verdict_reason", "Analysis finished.")
#                     report = parsed.get("analysis_report", "")
#         except json.JSONDecodeError as e:
#             return self._result(
#                 "FAILED", f"LLM returned unparseable JSON structural schema: {e}", 0.0, False,
#                 logs=logs + [f"[LLM Engine] Response formatting crashed parsing checks: {e}"],
#             )
#         except Exception as e:
#             return self._result(
#                 "FAILED", f"LLM execution channel failure: {e}", 0.0, False,
#                 logs=logs + [f"[LLM Engine] Run invocation failed: {e}"],
#             )

#         has_errors_majority = error_votes > self.consistency_runs / 2
#         vote_consensus_rate = max(error_votes, self.consistency_runs - error_votes) / self.consistency_runs
#         verdict_passed = not has_errors_majority

#         # Method 2 & 3: Combined Semantic Consistency & Self-Reflection Matrix
#         mean_critic_score = sum(critic_scores) / len(critic_scores) if critic_scores else 0.85
        
#         calculated_confidence = vote_consensus_rate * mean_critic_score
#         if not ast_ran:
#             calculated_confidence *= 0.95  # Standard structural extension penalty calibration

#         final_confidence = max(0.10, min(0.98, calculated_confidence))

#         logs.append(
#             f"[LLM Engine] Evaluated {self.consistency_runs} parallel consensus runs — flagged errors in {error_votes}/{self.consistency_runs} loops "
#             f"(Semantic consensus score: {vote_consensus_rate:.0%}, Mean Critic Certainty: {mean_critic_score:.2f})."
#         )
#         if truncated:
#             logs.append(
#                 f"[LLM Engine] Target exceeds context bounds — analysis limited to the leading {MAX_PROMPT_CHARS} characters."
#             )
#         logs.append(
#             f"[Gate Input] proposed verdict={'PASS' if verdict_passed else 'FAIL'}, confidence={final_confidence:.4f} "
#             f"(Calculated dynamically via combined consensus and internal critic parameters)."
#         )

#         return self._result(
#             "COMPLETED",
#             reason,
#             round(final_confidence, 2),
#             verdict_passed,
#             ai_analysis=report,
#             logs=logs,
#         )
















# import sys
# import os
# import json
# from pathlib import Path
# import ast

# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from core_platform.model_client import call_llm

# MAX_PROMPT_CHARS = 4000
# DEFAULT_CONSISTENCY_RUNS = 3  # Parallel execution threads for consensus verification

# class CodeDebuggerAgent:
#     def __init__(self, consistency_runs: int = DEFAULT_CONSISTENCY_RUNS):
#         self.consistency_runs = consistency_runs

#     def _verify_syntax_ast(self, file_path: Path, content: str) -> tuple[bool, str, bool]:
#         """
#         Deterministic syntax parser. Executes an authentic AST compilation trace
#         for Python resources, or seamlessly routes other programming languages to
#         the temperature-based semantic consensus matrix.
#         """
#         if file_path.suffix != ".py":
#             return (
#                 True,
#                 f"Static AST syntax verification bypassed — file extension '{file_path.suffix or 'none'}' "
#                 f"routed directly to multi-pass semantic consistency matrix.",
#                 False,
#             )
#         try:
#             ast.parse(content)
#             return True, "Parsed successfully with Python's ast module — no syntax errors.", True
#         except SyntaxError as e:
#             return False, f"ast.parse failed at line {e.lineno}, column {e.offset}: {e.msg}", True

#     def _ask_llm_once(self, content: str, extension: str, run_index: int) -> dict:
#         # Style variations simulate high-temperature semantic shifts inside the local model engine
#         analysis_modes = [
#             "Pass 1: Rigid Compiler Rule Check. Focus on standard layout and explicit compilation constraints.",
#             "Pass 2: Boundary Exception Check. Focus on data mutation logic and potential runtime errors.",
#             "Pass 3: Edge Case Verification. Focus on race conditions, types, and uncommon logical flow deadlocks."
#         ]
#         current_mode = analysis_modes[run_index if run_index < len(analysis_modes) else 1]
        
#         prompt = f"""You are an elite cross-compiler analysis engine inspecting source code strings for bugs, syntax errors, or logical faults.
# Target Language Framework/Extension Reference: {extension}
# Analysis Style Mode: {current_mode}
# ---
# {content[:MAX_PROMPT_CHARS]}
# ---
# CRITICAL INSTRUCTION: Analyze the text buffer carefully against standard compiler grammar and layout specifications for this language target.
# You must respond ONLY with a valid JSON object. Do not include markdown blocks, backticks, or trailing prose.

# The JSON structure must match this format precisely:
# {{
#     "has_errors": true or false,
#     "internal_certainty_score": 0.0 to 1.0,
#     "verdict_reason": "Clear one-sentence summary of the compilation status or major bug found",
#     "analysis_report": "Detailed architectural breakdown tracking detected anomalies, verified structural corrections, and technical causes"
# }}"""
#         raw = call_llm(prompt).strip()
#         if raw.startswith("```json"):
#             raw = raw[7:]
#         if raw.endswith("```"):
#             raw = raw[:-3]
#         return json.loads(raw.strip())

#     @staticmethod
#     def _result(status, reason, confidence, verdict, ai_analysis="", logs=None):
#         return {
#             "status": status,
#             "reason": reason,
#             "confidence": confidence,
#             "verdict": verdict,
#             "ai_analysis": ai_analysis,
#             "logs": logs or [],
#         }

#     def run(self, repo_path: str, mode: str = "automatic") -> dict:
#         file_path = Path(repo_path)
#         logs = ["[Orchestrator] Task debug_code initiated."]
        
#         # FIXED: Dynamic path resolution context block
#         # If the orchestrator targets a workspace directory, auto-detect app.py rather than skipping
#         if file_path.is_dir():
#             target_app = file_path / "app.py"
#             if target_app.exists():
#                 logs.append(f"[CodeDebuggerAgent] Target path is a directory. Resolved workspace core file: {target_app.name}")
#                 file_path = target_app
        
#         if not file_path.exists() or file_path.is_dir():
#             return self._result(
#                 "SKIPPED", 
#                 "Target path does not exist or is a directory.", 
#                 1.0, 
#                 True,
#                 logs=logs + ["[CodeDebuggerAgent] Target path not found — skipping workspace execution branch."],
#             )

#         try:
#             content = file_path.read_text(encoding="utf-8", errors="ignore")
#         except Exception as e:
#             return self._result(
#                 "FAILED", 
#                 f"Could not read file: {e}", 
#                 0.0, 
#                 False,
#                 logs=logs + [f"[CodeDebuggerAgent] System failure reading text buffer streams: {e}"],
#             )

#         if not content.strip():
#             return self._result(
#                 "FAILED", 
#                 "File is empty.", 
#                 0.0, 
#                 False,
#                 logs=logs + [f"[CodeDebuggerAgent] Content payload is empty for '{file_path.name}' — aborting verification."],
#             )

#         if mode == "manual_error":
#             return self._result(
#                 "FAILED", 
#                 "Manual failure simulation active.", 
#                 1.0, 
#                 False,
#                 ai_analysis="Simulated failure mode triggered for pipeline testing.",
#                 logs=logs + ["[CodeDebuggerAgent] manual_error override active — forcing gate failure verdict."],
#             )

#         ast_passed, ast_message, ast_ran = self._verify_syntax_ast(file_path, content)
#         truncated = len(content) > MAX_PROMPT_CHARS
#         logs.append(f"[AST Engine] {ast_message}")

#         if ast_ran and not ast_passed:
#             logs.append("[Gate Input] proposed verdict=FAIL, confidence=1.00 (Deterministic baseline violation found).")
#             return self._result(
#                 "COMPLETED",
#                 f"AST compiler intercepted structural fault: {ast_message}",
#                 1.0,
#                 False,
#                 logs=logs,
#             )

#         reason, report = "", ""
#         error_votes = 0
#         critic_scores = []
        
#         try:
#             for i in range(self.consistency_runs):
#                 parsed = self._ask_llm_once(content, file_path.suffix or ".txt", run_index=i)
                
#                 has_error = bool(parsed.get("has_errors", False))
#                 critic_score = float(parsed.get("internal_certainty_score", 0.85))
                
#                 critic_scores.append(critic_score)
#                 if has_error:
#                     error_votes += 1
                
#                 if i == 0:
#                     reason = parsed.get("verdict_reason", "Analysis finished.")
#                     report = parsed.get("analysis_report", "")
#         except json.JSONDecodeError as e:
#             return self._result(
#                 "FAILED", 
#                 f"LLM returned unparseable JSON structural schema: {e}", 
#                 0.0, 
#                 False,
#                 logs=logs + [f"[LLM Engine] Response formatting crashed parsing checks: {e}"],
#             )
#         except Exception as e:
#             return self._result(
#                 "FAILED", 
#                 f"LLM execution channel failure: {e}", 
#                 0.0, 
#                 False,
#                 logs=logs + [f"[LLM Engine] Run invocation failed: {e}"],
#             )

#         has_errors_majority = error_votes > self.consistency_runs / 2
#         vote_consensus_rate = max(error_votes, self.consistency_runs - error_votes) / self.consistency_runs
#         verdict_passed = not has_errors_majority

#         # Method 2 & 3: Combined Semantic Consistency & Self-Reflection Matrix
#         mean_critic_score = sum(critic_scores) / len(critic_scores) if critic_scores else 0.85
        
#         calculated_confidence = vote_consensus_rate * mean_critic_score
#         if not ast_ran:
#             calculated_confidence *= 0.95  # Standard structural extension penalty calibration
#         final_confidence = max(0.10, min(0.98, calculated_confidence))

#         logs.append(
#             f"[LLM Engine] Evaluated {self.consistency_runs} parallel consensus runs — flagged errors in {error_votes}/{self.consistency_runs} loops "
#             f"(Semantic consensus score: {vote_consensus_rate:.0%}, Mean Critic Certainty: {mean_critic_score:.2f})."
#         )
#         if truncated:
#             logs.append(f"[LLM Engine] Target exceeds context bounds — analysis limited to the leading {MAX_PROMPT_CHARS} characters.")

#         logs.append(
#             f"[Gate Input] proposed verdict={'PASS' if verdict_passed else 'FAIL'}, confidence={final_confidence:.4f} "
#             f"(Calculated dynamically via combined consensus and internal critic parameters)."
#         )

#         return self._result(
#             "COMPLETED",
#             reason,
#             round(final_confidence, 2),
#             verdict_passed,
#             ai_analysis=report,
#             logs=logs,
#         )



























import sys
import os
import json
from pathlib import Path
import ast

# Add the project root directory to sys.path so it can find core_platform modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core_platform.model_client import call_llm

MAX_PROMPT_CHARS = 4000
DEFAULT_CONSISTENCY_RUNS = 3  # Parallel execution threads for consensus verification

class CodeDebuggerAgent:
    def __init__(self, consistency_runs: int = DEFAULT_CONSISTENCY_RUNS):
        self.consistency_runs = consistency_runs

    def _verify_syntax_ast(self, file_path: Path, content: str) -> tuple[bool, str, bool]:
        """
        Deterministic syntax parser. Executes an authentic AST compilation trace
        for Python resources, or seamlessly routes other programming languages to
        the temperature-based semantic consensus matrix.
        """
        if file_path.suffix != ".py":
            return (
                True,
                f"Static AST syntax verification bypassed — file extension '{file_path.suffix or 'none'}' "
                f"routed directly to multi-pass semantic consistency matrix.",
                False,
            )
        try:
            ast.parse(content)
            return True, "Parsed successfully with Python's ast module — no syntax errors.", True
        except SyntaxError as e:
            return False, f"ast.parse failed at line {e.lineno}, column {e.offset}: {e.msg}", True

    def _ask_llm_once(self, content: str, extension: str, run_index: int) -> dict:
        # Style variations simulate high-temperature semantic shifts inside the local model engine
        analysis_modes = [
            "Pass 1: Rigid Compiler Rule Check. Focus on standard layout and explicit compilation constraints.",
            "Pass 2: Boundary Exception Check. Focus on data mutation logic and potential runtime errors.",
            "Pass 3: Edge Case Verification. Focus on race conditions, types, and uncommon logical flow deadlocks."
        ]
        current_mode = analysis_modes[run_index if run_index < len(analysis_modes) else 1]
        
        prompt = f"""You are an elite cross-compiler analysis engine inspecting source code strings for bugs, syntax errors, or logical faults.
Target Language Framework/Extension Reference: {extension}
Analysis Style Mode: {current_mode}
---
{content[:MAX_PROMPT_CHARS]}
---
CRITICAL INSTRUCTION: Analyze the text buffer carefully against standard
compiler grammar and layout specifications for this language target.
You must respond ONLY with a valid JSON object. Do not include markdown
blocks, backticks, or trailing prose.

The JSON structure must match this format precisely:
{{
    "has_errors": true or false,
    "internal_certainty_score": 0.0 to 1.0,
    "verdict_reason": "Clear one-sentence summary of the compilation status or major bug found",
    "analysis_report": "Detailed architectural breakdown tracking detected anomalies, verified structural corrections, and technical causes"
}}"""
        raw = call_llm(prompt).strip()
        if raw.startswith("```json"):
            raw = raw[7:]
        if raw.endswith("```"):
            raw = raw[:-3]
        return json.loads(raw.strip())

    @staticmethod
    def _result(status, reason, confidence, verdict, ai_analysis="", logs=None):
        return {
            "status": status,
            "reason": reason,
            "confidence": confidence,
            "verdict": verdict,
            "ai_analysis": ai_analysis,
            "logs": logs or [],
        }

    def run(self, repo_path: str, mode: str = "automatic") -> dict:
        file_path = Path(repo_path)
        logs = ["[Orchestrator] Task debug_code initiated."]
        
        # FIXED: Dynamic path resolution context block
        # If the orchestrator targets a workspace directory, auto-detect app.py rather than skipping
        if file_path.is_dir():
            target_app = file_path / "app.py"
            if target_app.exists():
                logs.append(f"[CodeDebuggerAgent] Target path is a directory. Resolved workspace core file: {target_app.name}")
                file_path = target_app
        
        if not file_path.exists() or file_path.is_dir():
            return self._result(
                "SKIPPED",
                "Target path does not exist or is a directory.",
                1.0,
                True,
                logs=logs + ["[CodeDebuggerAgent] Target path not found — skipping workspace execution branch."],
            )

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            return self._result(
                "FAILED",
                f"Could not read file: {e}",
                0.0,
                False,
                logs=logs + [f"[CodeDebuggerAgent] System failure reading text buffer streams: {e}"],
            )

        if not content.strip():
            return self._result(
                "FAILED",
                "File is empty.",
                0.0,
                False,
                logs=logs + [f"[CodeDebuggerAgent] Content payload is empty for '{file_path.name}' — aborting verification."],
            )

        if mode == "manual_error":
            return self._result(
                "FAILED",
                "Manual failure simulation active.",
                1.0,
                False,
                ai_analysis="Simulated failure mode triggered for pipeline testing.",
                logs=logs + ["[CodeDebuggerAgent] manual_error override active — forcing gate failure verdict."],
            )

        ast_passed, ast_message, ast_ran = self._verify_syntax_ast(file_path, content)
        truncated = len(content) > MAX_PROMPT_CHARS
        logs.append(f"[AST Engine] {ast_message}")

        if ast_ran and not ast_passed:
            # FIXED: Changed confidence output marker from 1.00 to 0.00 to reflect absolute broken compilation
            logs.append("[Gate Input] proposed verdict=FAIL, confidence=0.00 (Deterministic baseline violation found).")
            return self._result(
                "COMPLETED",
                f"AST compiler intercepted structural fault: {ast_message}",
                0.00,
                False,
                logs=logs,
            )

        reason, report = "", ""
        error_votes = 0
        critic_scores = []
        
        try:
            for i in range(self.consistency_runs):
                parsed = self._ask_llm_once(content, file_path.suffix or ".txt", run_index=i)
                
                has_error = bool(parsed.get("has_errors", False))
                critic_score = float(parsed.get("internal_certainty_score", 0.85))
                
                critic_scores.append(critic_score)
                if has_error:
                    error_votes += 1
                
                if i == 0:
                    reason = parsed.get("verdict_reason", "Analysis finished.")
                    report = parsed.get("analysis_report", "")
        except json.JSONDecodeError as e:
            return self._result(
                "FAILED",
                f"LLM returned unparseable JSON structural schema: {e}",
                0.0,
                False,
                logs=logs + [f"[LLM Engine] Response formatting crashed parsing checks: {e}"],
            )
        except Exception as e:
            return self._result(
                "FAILED",
                f"LLM execution channel failure: {e}",
                0.0,
                False,
                logs=logs + [f"[LLM Engine] Run invocation failed: {e}"],
            )

        has_errors_majority = error_votes > self.consistency_runs / 2
        vote_consensus_rate = max(error_votes, self.consistency_runs - error_votes) / self.consistency_runs
        verdict_passed = not has_errors_majority

        # Method 2 & 3: Combined Semantic Consistency & Self-Reflection Matrix
        mean_critic_score = sum(critic_scores) / len(critic_scores) if critic_scores else 0.85
        
        calculated_confidence = vote_consensus_rate * mean_critic_score
        if not ast_ran:
            calculated_confidence *= 0.95  # Standard structural extension penalty calibration
            
        final_confidence = max(0.10, min(0.98, calculated_confidence))
        
        # FIXED: If the majority consensus detects logical bugs, step down the final displayed metrics score
        if not verdict_passed:
            final_confidence = min(0.45, final_confidence)

        logs.append(
            f"[LLM Engine] Evaluated {self.consistency_runs} parallel consensus runs — flagged errors in {error_votes}/{self.consistency_runs} loops "
            f"(Semantic consensus score: {vote_consensus_rate:.0%}, Mean Critic Certainty: {mean_critic_score:.2f})."
        )
        if truncated:
            logs.append(f"[LLM Engine] Target exceeds context bounds — analysis limited to the leading {MAX_PROMPT_CHARS} characters.")

        logs.append(
            f"[Gate Input] proposed verdict={'PASS' if verdict_passed else 'FAIL'}, confidence={final_confidence:.4f} "
            f"(Calculated dynamically via combined consensus and internal critic parameters)."
        )

        return self._result(
            "COMPLETED",
            reason,
            round(final_confidence, 2),
            verdict_passed,
            ai_analysis=report,
            logs=logs,
        )
