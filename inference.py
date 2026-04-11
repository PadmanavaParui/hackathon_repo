import os
import json
import urllib.request

# The platform will inject the ENV_URL when grading
ENV_URL = os.getenv("ENV_URL", "http://127.0.0.1:8000")

def make_post_request(url, data=None):
    """Helper function to make POST requests using ONLY built-in Python libraries."""
    req = urllib.request.Request(url, method="POST")
    req.add_header("Content-Type", "application/json")
    
    data_bytes = json.dumps(data).encode("utf-8") if data else b"{}"
    
    try:
        with urllib.request.urlopen(req, data=data_bytes) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"HTTP Request failed: {e}", flush=True)
        raise

def run_baseline():
    task_name = "easy"
    # REQUIRED FORMAT: [START] task=NAME
    print(f"[START] task={task_name}", flush=True)
    
    try:
        obs = make_post_request(f"{ENV_URL}/reset", {"task_id": task_name})
    except Exception as e:
        print(f"Failed to reset environment: {e}", flush=True)
        return

    done = False
    step_count = 0
    max_steps = 24
    total_reward = 0.0

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
            total_reward += reward
            done = data.get("done", True)
            
            # REQUIRED FORMAT: [STEP] step=1 reward=0.5
            print(f"[STEP] step={step_count} reward={reward}", flush=True)
            
        except Exception as e:
            print(f"Step failed: {e}", flush=True)
            break

    # Calculate a dummy final score (0.0 to 1.0) based on reward
    final_score = max(0.0, min(1.0, total_reward / max_steps))
    
    # REQUIRED FORMAT: [END] task=NAME score=0.95 steps=1
    print(f"[END] task={task_name} score={final_score:.2f} steps={step_count}", flush=True)

if __name__ == "__main__":
    run_baseline()