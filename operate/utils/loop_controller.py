class LoopController:
    def __init__(self, decider, executor, max_steps: int = 20):
        self.decider = decider
        self.executor = executor
        self.max_steps = max_steps

    def run(self, state):
        """
        Main HumanOS loop:
        decide → execute → update → repeat
        """

        print(f"[HumanOS] Objective: {state.objective}")

        while True:
            # 1. Safety stop
            if state.step_count >= self.max_steps:
                raise RuntimeError("Max steps exceeded. Stopping to avoid infinite loop.")

            print(f"\n[HumanOS] Step {state.step_count}")

            # 2. Decide
            actions = self.decider.decide_next_action(state)

            if not actions or len(actions) == 0:
                raise RuntimeError("Decider returned no actions.")

            # 3. Execute actions sequentially
            for action in actions:
                print(f"[HumanOS] Executing: {action}")

                # Stop condition
                if action.action_type == "done":
                    print(f"[HumanOS] Done: {action.summary}")
                    return

                self.executor.execute(action)
                state.last_action = action

            # 4. Update state
            state.step_count += 1
