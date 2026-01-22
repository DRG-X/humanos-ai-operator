from operate.utils.loop_controller import LoopController
from operate.models.state import State
from operate.utils.executor import Executor
from operate.models.decider import LLMDecider
from operate.utils.operating_system import OperatingSystem
import logging
import os 
from datetime import datetime
import uuid

def setup_logging():
    LOG_DIR = "log/runs"
    os.makedirs(LOG_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(LOG_DIR, f"run_{timestamp}.log")


    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[ # handlers list means that where the log files will be sent 
            logging.FileHandler(log_file), # sends lod to specifies file 
            logging.StreamHandler() # sends logging to terminal 
        ]
    )

    logging.getLogger().info("LOGGING_INITIALIZED")
    logging.getLogger().info(f"Log file: {log_file}") # future me will thank me for using the longer line.. i could also have used looging.infO() instead of logging.getLogger().info()

    return log_file


def generate_run_id() -> str:
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    short_uid = uuid.uuid4().hex[:4]
    return (f"{ts}_{short_uid}")


def main():
    log_file = setup_logging()
    # 1. Get user objective
    objective = input("Enter objective for HumanOS: ").strip()
    run_id = generate_run_id()
    if not objective:
        raise ValueError("Objective cannot be empty")
    # 2. Initialize core components
    state = State(objective=objective , run_id = run_id)
    operating_system = OperatingSystem()
    executor = Executor(operating_system)

    decider = LLMDecider(model_name="gpt-4o")

    loop_controller = LoopController(
        decider=decider,
        executor=executor,
        max_steps=20
    )

    # 3. Start HumanOS
    loop_controller.run(state)


if __name__ == "__main__":
    main()
