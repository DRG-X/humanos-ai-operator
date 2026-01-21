class Executor:
    def __init__(self, operating_system):
        """
        operating_system: low-level OS controller
        (mouse, keyboard, etc.)
        """
        self.os = operating_system

    def execute(self, action):
        """
        Execute a single Action.
        Crashes fast if the action is invalid.
        """

        action_type = action.action_type

        if action_type == "click":
            if action.x is None or action.y is None:
                raise ValueError("Click action missing coordinates")

            self.os.click(action.x, action.y)
            return

        if action_type == "write":
            if action.text is None:
                raise ValueError("Write action missing text")

            self.os.write(action.text)
            return

        if action_type == "press":
            if not action.keys:
                raise ValueError("Press action missing keys")

            self.os.press(action.keys)
            return

        if action_type == "done":
            # Done is handled by loop controller, not executor
            return

        # Should never happen if Action is validated
        raise RuntimeError(f"Unknown action type: {action_type}")
