import json
import os
from datetime import datetime

def save_output(output: dict):
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output_{timestamp}.json"
    with open(f"output/{filename}", "w") as f:
        json.dump(output, f, indent=4)
