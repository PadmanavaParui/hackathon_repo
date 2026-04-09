from pydantic import BaseModel, Field
from typing import List, Optional

# --- Action Space ---
class Action(BaseModel):
    battery_flow: float = Field(..., ge=-1.0, le=1.0, description="-1.0 (discharge) to 1.0 (charge)")
    diesel_activation: float = Field(..., ge=0.0, le=1.0, description="0.0 (off) to 1.0 (max)")
    grid_trade: float = Field(..., ge=-1.0, le=1.0, description="-1.0 (sell) to 1.0 (buy)")
    shed_zone_load: int = Field(..., ge=0, le=2, description="0 (none), 1 (Zone A), 2 (Zone B)")

# --- Observation Space ---
class Observation(BaseModel):
    current_demand: float
    grid_frequency: float
    spot_price: float
    battery_soc: float
    solar_forecast: List[float]
    wind_forecast: List[float]

# --- API Payloads ---
class ResetRequest(BaseModel):
    task_id: Optional[str] = "easy"

class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: dict