import logging

logger = logging.getLogger(__name__)


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

        # print(f"[HumanOS] Objective: {state.objective}")
        logger.info(f"HumanOS Objective: {state.objective}")

        while True:
            # 1. Safety stop
            if state.step_count >= self.max_steps:
                logger.error("Agent stopped due to max steps exceeded." , 
                             extra = {
                                 "step": state.step_count,
                                "last_action": str(state.last_action)
                             })
                raise RuntimeError("Max steps exceeded. Stopping to avoid infinite loop.")
            # print(f"\n[HumanOS] Step {state.step_count}")
            logger.info(
                "Step Started" , 
                extra = {
                    "step": state.step_count , 
                    "last_action" : str(state.last_action)
                }
            )
            # 2. Decide
            actions = self.decider.decide_next_action(state)

            if not actions or len(actions) == 0:
                logger.error("Decider returned no actions.")
                raise RuntimeError("Decider returned no actions.")

            # 3. Execute actions sequentially
            for action in actions:
                # print(f"[HumanOS] Executing: {action}")
                logger.info(f"Executng Action: {action}")

                # Stop condition
                if action.action_type == "done":
                    # print(f"[HumanOS] Done: {action.summary}")
                    logger.info(f"Action Done: {action.summary}")
                    return
                try:
                    self.executor.execute(action)
                    logger.info(
                        "Action_Executed" , 
                        extra = {
                            "step": state.step_count,
                            "action_type": action.action_type
                        }
                    )
                except Exception:
                    logger.exception(
                        "Action_Execution_Failed",
                        extra = {
                            "step": state.step_count,
                            "action_type" : action.action_type
                        }
                    )
                    raise
                state.last_action = action

            # 4. Update state
            state.step_count += 1

            logger.info(
                "Step_ended" , 
                extra = {
                    "step" : state.step_count
                }
            )
