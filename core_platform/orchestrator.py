# import os
# import uuid
# import requests

# class Task:
#     def __init__(self, kind, repo_path, metadata=None):
#         self.id = str(uuid.uuid4())
#         self.kind = kind
#         self.repo_path = repo_path
#         self.metadata = metadata or {}

# class Orchestrator:
#     def __init__(self, gate, trace_store, gitea_client):
#         self.gate = gate
#         self.trace_store = trace_store
#         self.gitea_client = gitea_client

#     def run_task(self, task, agent, mode="automatic"):
#         print(f"\n[Orchestrator] Starting task: {task.kind} on {task.repo_path} ({mode} mode)")
#         steps_completed = ["Repository Validation Passed"]
        
#         # Execute the agent — now calls real Ollama and scans files
#         agent_result = agent.run(task.repo_path, mode=mode)
        
#         # Print the streaming AI text output onto the Windows command window
#         if "ai_analysis" in agent_result:
#             print("\n" + "="*60)
#             print(f"[AI ANALYSIS — {task.kind.upper()}]")
#             print(agent_result["ai_analysis"][:1500])
#             print("="*60 + "\n")
            
#         # Parse metrics directly from our structural task kinds
#         if task.kind == "dependency_upgrade":
#             steps_completed.append("Dependency Agent Analysis Completed")
#             issues = agent_result.get("issues_found", 0)
#             confidence = max(0.5, 1.0 - (issues * 0.05))
#             reasons = [
#                 f"Found {issues} outdated package dependencies.",
#                 agent_result.get("reason", "")
#             ]
#         elif task.kind == "test_triage":
#             steps_completed.append("Test Triage Agent Analysis Completed")
#             failed = agent_result.get("failed_tests", 0)
#             confidence = max(0.5, 1.0 - (failed * 0.1))
#             reasons = [
#                 f"Detected test suite anomalies. Failures: {failed}.",
#                 agent_result.get("reason", "")
#             ]
#         elif task.kind == "generate_docs":
#             steps_completed.append("Documentation Agent Analysis Completed")
#             confidence = 0.95
#             reasons = [
#                 agent_result.get("reason", "Code documentation parsed successfully.")
#             ]
#         elif task.kind == "debug_code":
#             steps_completed.append("Source Code Debugger Verification Finished")
#             confidence = 0.95
#             reasons = [
#                 agent_result.get("reason", "Source text stream checked successfully.")
#             ]
#         else:  # code_review
#             steps_completed.append("Review Agent Analysis Completed")
#             confidence = 0.90
#             reasons = [
#                 agent_result.get("reason", "Structural code review completed successfully.")
#             ]

#         # Extract explicit boolean run verdicts
#         gate_passed = agent_result.get("verdict", True)
#         status_str = agent_result.get("status", "COMPLETED")

#         trace = {
#             "run_id": task.id,
#              "task_id": task.id,
#             "task": task.kind,
#              "repo": task.repo_path,
#              "status": status_str,
#              "state": status_str,
#              "verdict": gate_passed,
#              "confidence": round(confidence, 2),
#              "pr_url": f"http://127.0.0.1:3000/agent-bot/{os.path.basename(task.repo_path)}/pulls/1",
#              "reasons": [r for r in reasons if r.strip()],
#              "steps": steps_completed,
#              "agent_detail": agent_result
#          }

#         trace = {
#             "run_id": task.id,
#             "task_id": task.id,
#             "task": task.kind,
#             "repo": task.repo_path,
#             "status": status_str,
#             "state": status_str,
#             "verdict": gate_passed,
#             "gate_verdict": "PASSED" if gate_passed else "FAILED",  # <-- ADD THIS LINE
#             "confidence": round(confidence, 2),
#             "pr_url": f"http://127.0.0.1:3000/agent-bot/{os.path.basename(task.repo_path)}/pulls/1",
#             "reasons": [r for r in reasons if r.strip()],
#             "steps": steps_completed,
#             "agent_detail": agent_result
#         }
        
#         self.trace_store.save_trace(trace)
        
#         try:
#             requests.post("http://127.0.0.1:8000/api/traces", json=trace, timeout=5)
#         except Exception as e:
#             print(f"[Orchestrator] Dashboard transmission note: {e}")
            
#         print(f"[Orchestrator] Task {task.id} finished with status: {status_str}.")
#         return trace









# import os
# import uuid
# import requests

# class Task:
#     def __init__(self, kind, repo_path, metadata=None):
#         self.id = str(uuid.uuid4())
#         self.kind = kind
#         self.repo_path = repo_path
#         self.metadata = metadata or {}

# class Orchestrator:
#     def __init__(self, gate, trace_store, gitea_client):
#         self.gate = gate
#         self.trace_store = trace_store
#         self.gitea_client = gitea_client

#     def run_task(self, task, agent, mode="automatic"):
#         print(f"\n[Orchestrator] Starting task: {task.kind} on {task.repo_path} ({mode} mode)")
#         steps_completed = ["Repository Validation Passed"]
        
#         # Execute the agent — now calls real Ollama and scans files
#         agent_result = agent.run(task.repo_path, mode=mode)
        
#         # Print the streaming AI text output onto the Windows command window
#         if "ai_analysis" in agent_result:
#             print("\n" + "="*60)
#             print(f"[AI ANALYSIS — {task.kind.upper()}]")
#             print(agent_result["ai_analysis"][:1500])
#             print("="*60 + "\n")
            
#         # Parse metrics directly from our structural task kinds
#         if task.kind == "dependency_upgrade":
#             steps_completed.append("Dependency Agent Analysis Completed")
#             issues = agent_result.get("issues_found", 0)
#             confidence = max(0.5, 1.0 - (issues * 0.05))
#             reasons = [
#                 f"Found {issues} outdated package dependencies.",
#                 agent_result.get("reason", "")
#             ]
#         elif task.kind == "test_triage":
#             steps_completed.append("Test Triage Agent Analysis Completed")
#             failed = agent_result.get("failed_tests", 0)
#             confidence = max(0.5, 1.0 - (failed * 0.1))
#             reasons = [
#                 f"Detected test suite anomalies. Failures: {failed}.",
#                 agent_result.get("reason", "")
#             ]
#         elif task.kind == "generate_docs":
#             steps_completed.append("Documentation Agent Analysis Completed")
#             confidence = 0.95
#             reasons = [
#                 agent_result.get("reason", "Code documentation parsed successfully.")
#             ]
#         elif task.kind == "debug_code":
#             steps_completed.append("Source Code Debugger Verification Finished")
#             confidence = 0.95
#             reasons = [
#                 agent_result.get("reason", "Source text stream checked successfully.")
#             ]
#         else:  # code_review
#             steps_completed.append("Review Agent Analysis Completed")
#             confidence = 0.90
#             reasons = [
#                 agent_result.get("reason", "Structural code review completed successfully.")
#             ]

#         # Extract explicit boolean run verdicts
#         gate_passed = agent_result.get("verdict", True)
#         status_str = agent_result.get("status", "COMPLETED")

#         trace = {
#             "run_id": task.id,
#             "task_id": task.id,
#             "task": task.kind,
#             "repo": task.repo_path,
#             "status": status_str,
#             "state": status_str,
#             "verdict": gate_passed,
#             "gate_verdict": "PASSED" if gate_passed else "FAILED",
#             "confidence": round(confidence, 2),
#             "pr_url": f"http://127.0.0.1:3000/agent-bot/{os.path.basename(task.repo_path)}/pulls/1",
#             "reasons": [r for r in reasons if r.strip()],
#             "steps": steps_completed,
#             "agent_detail": agent_result,
#             # Pull dynamic telemetry step logs from the agent result if they exist, else fall back to steps_completed
#             "logs": agent_result.get("logs", steps_completed)
#         }
        
#         self.trace_store.save_trace(trace)
        
#         try:
#             requests.post("http://127.0.0.1:8000/api/traces", json=trace, timeout=5)
#         except Exception as e:
#             print(f"[Orchestrator] Dashboard transmission note: {e}")
            
#         print(f"[Orchestrator] Task {task.id} finished with status: {status_str}.")
#         return trace


















import os
import uuid
import requests

class Task:
    def __init__(self, kind, repo_path, metadata=None):
        self.id = str(uuid.uuid4())
        self.kind = kind
        self.repo_path = repo_path
        self.metadata = metadata or {}

class Orchestrator:
    def __init__(self, gate, trace_store, gitea_client):
        self.gate = gate
        self.trace_store = trace_store
        self.gitea_client = gitea_client

    def run_task(self, task, agent, mode="automatic"):
        print(f"\n[Orchestrator] Starting task: {task.kind} on {task.repo_path} ({mode} mode)")
        
        # Execute the agent — evaluates file data stream via AST engine and LLM verification matrices
        agent_result = agent.run(task.repo_path, mode=mode)
        
        if "ai_analysis" in agent_result:
            print("\n" + "="*60)
            print(f"[AI ANALYSIS — {task.kind.upper()}]")
            print(agent_result["ai_analysis"][:1500])
            print("="*60 + "\n")
            
        # Extract evaluation constraints
        confidence = agent_result.get("confidence", 0.0)
        gate_passed = agent_result.get("verdict", True)
        status_str = agent_result.get("status", "COMPLETED")
        reasons = [agent_result.get("reason", "")]

        trace = {
            "run_id": task.id,
            "task_id": task.id,
            "task": task.kind,
            "repo": task.repo_path,
            "status": status_str,
            "state": status_str,
            "verdict": gate_passed,
            "gate_verdict": "PASSED" if gate_passed else "FAILED",
            "confidence": round(confidence, 2),
             # "pr_url": f"http://127.0.0.1:3000/agent-bot/{os.path.basename(task.repo_path)}/pulls/1",
            "reasons": [r for r in reasons if r.strip()],
            "steps": agent_result.get("logs", ["Repository Validation Passed"]),
            "agent_detail": agent_result,
            "logs": agent_result.get("logs", ["[Orchestrator] Trace evaluation complete."])
        }
        
        self.trace_store.save_trace(trace)
        
        try:
            requests.post("http://127.0.0.1:8000/api/traces", json=trace, timeout=5)
        except Exception as e:
            print(f"[Orchestrator] Dashboard transmission note: {e}")
            
        print(f"[Orchestrator] Task {task.id} finished with status: {status_str}.")
        return trace