from typing import List, Optional, Dict, Any

# Allowed action names (hard contract)
ALLOWED_ACTIONS = {"click", "write", "press", "done"}


class Action:
    """
    Action is the strict contract between the LLM and the executor.
    If parsing fails here, the LLM output is invalid.
    """

    def __init__(
        self,
        action_type: str,
        x: Optional[float] = None,
        y: Optional[float] = None,
        text: Optional[str] = None,
        keys: Optional[List[str]] = None,
        summary: Optional[str] = None,
    ):
        self.action_type = action_type
        self.x = x
        self.y = y
        self.text = text
        self.keys = keys
        self.summary = summary

    # ---------- Parsing & Validation ----------

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Action":
        """
        Convert raw LLM JSON output into a validated Action.
        Crashes fast if anything is wrong.
        """

        if not isinstance(data, dict):
            raise ValueError("Action must be a JSON object")

        if "operation" not in data:
            raise ValueError("Missing 'operation' field in action")

        action_type = data["operation"]

        if action_type not in ALLOWED_ACTIONS:
            raise ValueError(f"Invalid action type: {action_type}")

        # ---- CLICK ----
        if action_type == "click":
            if "x" not in data or "y" not in data:
                raise ValueError("Click action requires 'x' and 'y'")

            return Action(
                action_type="click",
                x=float(data["x"]),
                y=float(data["y"]),
            )

        # ---- WRITE ----
        if action_type == "write":
            if "content" not in data:
                raise ValueError("Write action requires 'content'")

            return Action(
                action_type="write",
                text=str(data["content"]),
            )

        # ---- PRESS ----
        if action_type == "press":
            if "keys" not in data or not isinstance(data["keys"], list):
                raise ValueError("Press action requires 'keys' as a list")

            return Action(
                action_type="press",
                keys=[str(k) for k in data["keys"]],
            )

        # ---- DONE ----
        if action_type == "done":
            if "summary" not in data:
                raise ValueError("Done action requires 'summary'")

            return Action(
                action_type="done",
                summary=str(data["summary"]),
            )

        # This should never happen
        raise RuntimeError("Unhandled action type")

    # ---------- Debug / Logging ----------

    def __repr__(self) -> str:
        return f"Action({self.action_type}, x={self.x}, y={self.y}, text={self.text}, keys={self.keys}, summary={self.summary})"
