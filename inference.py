import os
import requests

ENV_URL = os.getenv("ENV_URL", "http://127.0.0.1:8000")

def run_baseline():
    print(f"Starting baseline agent against {ENV_URL}...")
    try:
        reset_response = requests.post(f"{ENV_URL}/reset", json={"task_id": "easy"})
        reset_response.raise_for_status()
        print(f"Initial Observation: {reset_response.json()}")
    except Exception as e:
        print(f"Failed to reset environment: {e}")
        return

    done = False
    step_count = 0
    while not done and step_count < 24:
        step_count += 1
        action = {"battery_flow": 0.5, "diesel_activation": 0.0, "grid_trade": 0.0, "shed_zone_load": 0}
        try:
            step_response = requests.post(f"{ENV_URL}/step", json=action)
            step_response.raise_for_status()
            data = step_response.json()
            done = data.get("done", True)
            print(f"Step {step_count} | Reward: {data.get('reward', 0.0)} | Done: {done}")
        except Exception as e:
            print(f"Step failed: {e}")
            break
    print("Baseline inference complete.")

if __name__ == "__main__":
    run_baseline()