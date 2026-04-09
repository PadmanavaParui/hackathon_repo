import math
from schema import Action, Observation

class PowerGridEnv:
    def __init__(self):
        self.timestep = 0
        self.max_steps = 24
        self.task_id = "easy"
        self.current_obs = None

    def reset(self, task_id: str) -> Observation:
        self.timestep = 0
        self.task_id = task_id
        
        # Phase 3: Task Design loading
        if task_id == "hard":
            solar = [0.0] * 5
            soc = 0.2
        else:
            solar = [100.0, 110.0, 120.0, 100.0, 80.0]
            soc = 0.8

        self.current_obs = Observation(
            current_demand=1000.0,
            grid_frequency=50.0,
            spot_price=0.15,
            battery_soc=soc,
            solar_forecast=solar,
            wind_forecast=[50.0, 45.0, 40.0, 30.0, 20.0]
        )
        return self.current_obs

    def step(self, action: Action) -> tuple[Observation, float, bool, dict]:
        self.timestep += 1
        
        # --- PHYSICS ENGINE (Phase 2) ---
        # Example calculation: if demand > supply, frequency drops
        supply_change = action.battery_flow + action.diesel_activation + action.grid_trade
        new_frequency = 50.0 + (supply_change * 0.1) # Simplified physics proxy
        
        # --- REWARD FUNCTION (Phase 4) ---
        delta_f = abs(50.0 - new_frequency)
        freq_stability = math.exp(-1.0 * delta_f)
        cost = action.diesel_activation * 0.5 + max(0, action.grid_trade * self.current_obs.spot_price)
        emissions = action.diesel_activation * 0.8
        survival_bonus = 0.1
        
        reward = freq_stability - cost - emissions + survival_bonus
        
        # --- TERMINATION ---
        done = False
        if new_frequency < 49.0 or new_frequency > 51.0 or self.timestep >= self.max_steps:
            done = True

        # Update State
        self.current_obs.grid_frequency = new_frequency
        
        return self.current_obs, reward, done, {"timestep": self.timestep}