import json
import os

def save_output(output: dict, filename="output.json"):
    os.makedirs("output", exist_ok=True)
    with open(f"output/{filename}", "w") as f:
        json.dump(output, f, indent=4)
