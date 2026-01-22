class State:
    def __init__(self, objective: str ,run_id : str ):
        if not objective or not isinstance(objective, str):
            raise ValueError("State requires a non-empty objective")

        self.objective = objective
        self.last_action = None
        self.step_count = 0
        self.run_id = run_id

    def increment_step(self):
        self.step_count += 1
