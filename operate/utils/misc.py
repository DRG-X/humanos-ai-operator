def convert_percent_to_decimal(percent: float) -> float:
    """
    Converts a percentage (0-100) to a decimal (0.0-1.0).
    Returns None if input is invalid.
    """
    try:
        if not isinstance(percent, (int, float)):
            return None
        if percent < 0 or percent > 100:
            return None
        return percent / 100.0
    except Exception as e :
        print("[percent_to_decimal] error:", e)
        return None
    

def build_system_prompt() -> str:
    return """
You are an AI that operates a computer by issuing structured actions.

You MUST respond with valid JSON ONLY.
The JSON MUST be an object with this exact structure:

{
  "actions": [
    { "type": "...", "...": "..." }
  ]
}

Allowed actions:

1. click
   { "type": "click", "x": float, "y": float }
   - x and y are screen coordinates between 0.0 and 1.0

2. write
   { "type": "write", "text": string }

3. press
   { "type": "press", "keys": [string] }

4. done
   { "type": "done", "summary": string }

Rules:
- Do NOT include explanations
- Do NOT include markdown or code fences
- If the task is complete, return exactly one action of type "done"
""".strip()


def build_user_prompt(state) -> str:
    """
    User-level prompt describing the current task and context.
    """

    last_action_text = (
        state.last_action if state.last_action else "None"
    )

    return f"""
Objective:
{state.objective}

Last action taken:
{last_action_text}

You are looking at the current screen.
Decide the next best action to move toward completing the objective.
""".strip()
