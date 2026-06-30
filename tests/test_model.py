import sys
import os

# Allow Python to see the platform folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core_platform.model_client import query_local_model

print("Sending test prompt to Qwen...")
response = query_local_model("Respond with only the word 'Success!' if you can read this.")
print("\nModel Response:")
print(response)