import os
import json
import urllib.request

# The platform will inject the ENV_URL when grading
ENV_URL = os.getenv("ENV_URL", "http://127.0.0.1:8000")

def make_post_request(url, data=None):
    """Helper function to make POST requests using ONLY built-in Python libraries."""
    req = urllib.request.Request(url, method="POST")
    req.add_header("Content-Type", "application/json")
    
    # Convert dictionary to JSON bytes
    data_bytes = json.dumps(data).encode("utf-8") if data else b"{}"
    
    try:
        with urllib.request.urlopen(req, data=data_bytes) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"HTTP Request failed: {e}")
        raise

def run_baseline():
    print(f"Starting baseline agent against {ENV_URL}...")
    
    # 1. Reset Environment
    try:
        obs = make_post_request(f"{ENV_URL}/reset", {"task_id": "easy"})
        print(f"Initial Observation: {obs}")
    except Exception as e:
        print(f"Failed to reset environment: {e}")
        return

    done = False
    step_count = 0
    max_steps = 24

    # 2. Step Loop
    while not done and step_count < max_steps:
        step_count += 1
        
        # Rule-based heuristic action
        action = {
            "battery_flow": 0.5,
            "diesel_activation": 0.0,
            "grid_trade": 0.0,
            "shed_zone_load": 0
        }
        
        try:
            data = make_post_request(f"{ENV_URL}/step", action)
            reward = data.get("reward", 0.0)
            done = data.get("done", True)
            print(f"Step {step_count} | Reward: {reward} | Done: {done}")
            
        except Exception as e:
            print(f"Step failed: {e}")
            break

    print("Baseline inference complete.")

if __name__ == "__main__":
    run_baseline()