import argparse
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Updated to use core_platform instead of platform
from core_platform.orchestrator import Orchestrator, Task
from core_platform.gate          import ReliabilityGate
from core_platform.trace_store   import TraceStore
from core_platform.gitea_client  import GiteaClient
from agents.dependency_agent  import DependencyAgent
from agents.test_triage_agent import TestTriageAgent
from agents.review_agent      import ReviewAgent
from agents.docs_agent import DocsAgent
from agents.code_debugger_agent import CodeDebuggerAgent
def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Reliability Platform")
    parser.add_argument("--task", choices=["dependency_upgrade", "test_triage", "code_review", "generate_docs", "debug_code"], required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--package", default="Flask")
    args = parser.parse_args()

    repo_path = os.path.abspath(args.repo)
   
    if not os.path.exists(args.repo):
       print(f"ERROR: repo path not found: {args.repo}")
       sys.exit(1)

    gate = ReliabilityGate(allowed_file_globs=["requirements.txt", "tests/*.py", "app/*.py"])
    trace_store = TraceStore()
    gitea = GiteaClient()
    orchestrator = Orchestrator(gate, trace_store, gitea)

    task = Task(kind=args.task, repo_path=repo_path, metadata={"package": args.package})

    agents = {
        "dependency_upgrade": DependencyAgent(),
        "test_triage":        TestTriageAgent(),
        "code_review":        ReviewAgent(),
        "generate_docs": DocsAgent(),
        "debug_code": CodeDebuggerAgent()
    }

    result = orchestrator.run_task(task, agents[args.task])

    print("\n" + "=" * 55)
    print("RESULT")
    print(f"  Task ID    : {result['task_id']}")
    print(f"  Final state: {result['state']}")
    print(f"  Gate       : {'PASSED ✅' if result['verdict'] else 'FAILED ❌'}")
    print(f"  Confidence : {result['confidence']:.1f}")
    # print(f"  PR URL     : {result['pr_url']}")
    if result["reasons"]:
        print("  Reasons:")
        for r in result["reasons"]:
            print(f"    - {r}")
    print("=" * 55)

if __name__ == "__main__":
    main()