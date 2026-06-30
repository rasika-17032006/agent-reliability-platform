import json
import os

class TraceStore:
    def __init__(self, storage_file="traces.json"):
        self.storage_file = storage_file
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, 'w') as f:
                json.dump([], f)

    def save_trace(self, trace_data):
        with open(self.storage_file, 'r+') as f:
            data = json.load(f)
            data.append(trace_data)
            f.seek(0)
            json.dump(data, f, indent=4)