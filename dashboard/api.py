# # import os
# # from fastapi import FastAPI
# # from fastapi.responses import FileResponse
# # from pydantic import BaseModel

# # app = FastAPI()

# # # A simple in-memory storage list for traces
# # TRACES_STORAGE = []

# # @app.get("/")
# # def read_root():
# #     return FileResponse("dashboard/static/dashboard.html")

# # @app.get("/api/traces")
# # def get_traces():
# #     return TRACES_STORAGE

# # @app.post("/api/traces")
# # def add_trace(trace: dict):
# #     TRACES_STORAGE.append(trace)
# #     return {"status": "success", "count": len(TRACES_STORAGE)}
# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)





# import os
# import json
# import uvicorn
# from fastapi import FastAPI, Request
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse

# app = FastAPI()

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# STATIC_DIR = os.path.join(BASE_DIR, "static")

# PROJECT_ROOT = os.path.dirname(BASE_DIR)
# TRACE_PATH = os.path.join(PROJECT_ROOT, "core_platform", "latest_trace.json")

# app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# @app.get("/")
# async def read_index():
#     return FileResponse(os.path.join(STATIC_DIR, "dashboard.html"))

# @app.get("/api/traces")
# async def get_traces():
#     if os.path.exists(TRACE_PATH):
#         with open(TRACE_PATH, "r") as f:
#             try:
#                 return json.load(f)
#             except json.JSONDecodeError:
#                 return []
    
#     # Clean fallback matching 'my_code.txt' if file doesn't exist yet
#     return {
#         "task_id": "a3efbaa0f18c4b9d88392cf99b3c548a",
#         "target_resource": "my_code.txt",
#         "gate_verdict": "FAILED",
#         "verdict": False,
#         "confidence": 0.90,
#         "reason": "The code contains a syntax error in the declaration of 'number'. It should be an integer type but was initialized with a String value."
#     }

# @app.post("/api/traces")
# async def save_trace(request: Request):
#     trace_data = await request.json()
    
#     traces = []
#     if os.path.exists(TRACE_PATH):
#         with open(TRACE_PATH, "r") as f:
#             try:
#                 traces = json.load(f)
#                 if not isinstance(traces, list):
#                     traces = [traces]
#             except json.JSONDecodeError:
#                 traces = []
                
#     traces.append(trace_data)
    
#     os.makedirs(os.path.dirname(TRACE_PATH), exist_ok=True)
#     with open(TRACE_PATH, "w") as f:
#         json.dump(traces, f, indent=4)
        
#     return {"status": "success"}

# if __name__ == "__main__":
#     uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
















# import os
# import json
# import uvicorn
# import subprocess
# from fastapi import FastAPI, Request, HTTPException
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse

# app = FastAPI()

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# STATIC_DIR = os.path.join(BASE_DIR, "static")

# PROJECT_ROOT = os.path.dirname(BASE_DIR)
# TRACE_PATH = os.path.join(PROJECT_ROOT, "core_platform", "latest_trace.json")

# app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# @app.get("/")
# async def read_index():
#     return FileResponse(os.path.join(STATIC_DIR, "dashboard.html"))

# @app.get("/api/traces")
# async def get_traces():
#     if os.path.exists(TRACE_PATH):
#         with open(TRACE_PATH, "r") as f:
#             try:
#                 return json.load(f)
#             except json.JSONDecodeError:
#                 return []
    
#     return {
#         "task_id": "a3efbaa0f18c4b9d88392cf99b3c548a",
#         "target_resource": "my_code.txt",
#         "gate_verdict": "FAILED",
#         "verdict": False,
#         "confidence": 0.90,
#         "reason": "The code contains a syntax error in the declaration of 'number'. It should be an integer type but was initialized with a String value."
#     }

# @app.post("/api/traces")
# async def save_trace(request: Request):
#     trace_data = await request.json()
    
#     traces = []
#     if os.path.exists(TRACE_PATH):
#         with open(TRACE_PATH, "r") as f:
#             try:
#                 traces = json.load(f)
#                 if not isinstance(traces, list):
#                     traces = [traces]
#             except json.JSONDecodeError:
#                 traces = []
                
#     traces.append(trace_data)
    
#     os.makedirs(os.path.dirname(TRACE_PATH), exist_ok=True)
#     with open(TRACE_PATH, "w") as f:
#         json.dump(traces, f, indent=4)
        
#     return {"status": "success"}

# @app.post("/api/commit-fix")
# async def commit_fix():
#     try:
#         repo_path = r"C:\Users\91867\agent-reliability-platform\e-commerce-payment-api"
        
#         status_check = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, cwd=repo_path)
        
#         if not status_check.stdout.strip():
#             return {"status": "success", "message": "Repository is already up-to-date. Nothing to commit."}
        
#         subprocess.run(["git", "add", "."], check=True, cwd=repo_path)
#         subprocess.run(["git", "commit", "-m", "fix: structural hotfix patch applied via autonomous agent gateway"], check=True, cwd=repo_path)
#         subprocess.run(["git", "push", "origin", "main"], check=True, cwd=repo_path)
        
#         return {"status": "success", "message": "Patch committed and pushed successfully"}
        
#     except subprocess.CalledProcessError as e:
#         raise HTTPException(status_code=500, detail=f"Git command execution failed: {str(e)}")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# if __name__ == "__main__":
#     uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)

























import os
import json
import uvicorn
import subprocess
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
PROJECT_ROOT = os.path.dirname(BASE_DIR)
TRACE_PATH = os.path.join(PROJECT_ROOT, "core_platform", "latest_trace.json")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(STATIC_DIR, "dashboard.html"))

@app.get("/api/traces")
async def get_traces():
    if os.path.exists(TRACE_PATH):
        with open(TRACE_PATH, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
 
    return {
        "task_id": "a3efbaa0f18c4b9d88392cf99b3c548a",
        "target_resource": "my_code.txt",
        "gate_verdict": "FAILED",
        "verdict": False,
        "confidence": 0.90,
        "reason": "The code contains a syntax error in the declaration of 'number'. It should be an integer type but was initialized with a String value."
    }

@app.post("/api/traces")
async def save_trace(request: Request):
    trace_data = await request.json()
 
    traces = []
    if os.path.exists(TRACE_PATH):
        with open(TRACE_PATH, "r") as f:
            try:
                traces = json.load(f)
                if not isinstance(traces, list):
                    traces = [traces]
            except json.JSONDecodeError:
                traces = []
 
    traces.append(trace_data)
 
    os.makedirs(os.path.dirname(TRACE_PATH), exist_ok=True)
    with open(TRACE_PATH, "w") as f:
        json.dump(traces, f, indent=4)
 
    return {"status": "success"}

@app.post("/api/commit-fix")
async def commit_fix():
    try:
        repo_path = r"C:\Users\91867\agent-reliability-platform\e-commerce-payment-api"
        target_file = os.path.join(repo_path, "app.py")
        
        # 1. Fully fixed production microservice logic to be injected programmatically
        fixed_code = """import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock database tracking a user account balance
ACCOUNTS_DB = {"user_123": {"balance": 500.0, "currency": "USD"}}

@app.route("/", methods=["GET"])
def homepage():
    return jsonify({"message": "Welcome to the Payment API Engine"}), 200

@app.route("/api/v1/checkout", methods=["POST"])
def process_checkout():
    data = request.json or {}
    user_id = data.get("user_id", "user_123")
    
    # Ensure amount is treated as a float, defaulting to 0 if missing
    try:
        amount = float(data.get("amount", 0))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid amount payload format"}), 400

    # FIX 1: Boundary validation implemented to completely block negative integers
    if amount <= 0:
        return jsonify({"status": "declined", "reason": "Charge amount must be positive"}), 400

    user_account = ACCOUNTS_DB.get(user_id)
    if not user_account:
        return jsonify({"status": "declined", "reason": "User profile missing"}), 404
        
    if user_account["balance"] < amount:
        return jsonify({"status": "declined", "reason": "Insufficient funds"}), 400
        
    user_account["balance"] -= amount
    
    # FIX 2: Safely wrapped file streams inside a standard contextual block manager
    try:
        with open("transaction_history.log", "a") as log_file:
            log_file.write(f"Processed: {user_id} charged {amount}\\n")
    except IOError as e:
        print(f"Logging failed: {e}")

    return jsonify({
        "status": "success",
        "remaining_balance": user_account["balance"]
    }), 200

if __name__ == "__main__":
    app.run(port=8080)
"""
        
        # 2. Programmatically apply the hotfix text stream directly onto disk
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(fixed_code)
            
        print(f"[Orchestrator] Applied autonomous text patch to {target_file}")

        # 3. Stage changes, commit, and push directly to local version control repository
        subprocess.run(["git", "add", "."], check=True, cwd=repo_path)
        
        status_check = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, cwd=repo_path)
        if not status_check.stdout.strip():
            return {"status": "success", "message": "Code updated locally, repository was already up-to-date."}
            
        subprocess.run(["git", "commit", "-m", "fix: structural hotfix patch applied via autonomous agent gateway"], check=True, cwd=repo_path)
        subprocess.run(["git", "push", "origin", "main"], check=True, cwd=repo_path)
        
        return {"status": "success", "message": "Patch committed and pushed successfully"}
        
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Git command execution failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)