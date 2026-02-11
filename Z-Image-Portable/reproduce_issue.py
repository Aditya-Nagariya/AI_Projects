# pyre-ignore-all-errors
import json
import requests
import uuid
import time

def queue_prompt(prompt_workflow):
    p = {"prompt": prompt_workflow, "client_id": str(uuid.uuid4())}
    try:
        response = requests.post("http://127.0.0.1:8189/prompt", json=p)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    try:
        with open("Z-Image-Workflow-API.json", "r") as f:
            workflow = json.load(f)
        
        print("Sending API-formatted workflow to server...")
        queue_prompt(workflow)
    except FileNotFoundError:
        print("Error: Z-Image-Workflow-API.json not found. Run convert_workflow.py first.")
