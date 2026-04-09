from fastapi import FastAPI, Request
from schema import Action, ResetRequest, StepResult
from environment import PowerGridEnv

app = FastAPI(title="Power Grid Demand-Response Optimizer API")
env = PowerGridEnv()

@app.post("/reset", response_model=dict)
async def reset_env(request: Request):
    # Safely handle missing bodies from strict auto-graders
    try:
        body = await request.json()
        task_id = body.get("task_id", "easy")
    except:
        task_id = "easy"
        
    obs = env.reset(task_id)
    return obs.model_dump()

@app.post("/step", response_model=StepResult)
async def step_env(action: Action):
    # Pass the validated Pydantic action to the physics engine
    obs, reward, done, info = env.step(action)
    
    return StepResult(
        observation=obs,
        reward=reward,
        done=done,
        info=info
    )

def start_server():
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    start_server()