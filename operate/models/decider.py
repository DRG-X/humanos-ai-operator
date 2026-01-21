# Given the current state of the world, ask the LLM what to ddo next and return structured actions 
from typing import List
import json
import base64
from openai import OpenAI

from operate.models.actions import Action
from operate.utils.screenshot import capture_and_optimize_screen
from operate.utils.misc import build_system_prompt, build_user_prompt



client = OpenAI()


def extract_json(text: str) -> str:
    if not text or not text.strip():
        raise ValueError("Input text is empty")

    text = text.strip()

    if text.startswith("```"):
        text = text.strip("`")
        text = text.replace("json", "").strip()

    first_obj = text.find("{")
    last_obj = text.rfind("}")

    if first_obj == -1 or last_obj == -1 or last_obj < first_obj:
        raise ValueError("No valid JSON object found")

    return text[first_obj:last_obj + 1]



class LLMDecider: 
    def __init__(self , model_name: str):
        self.model = model_name

    def decide_next_action(self , state) -> List[Action]:
        """
        Given the current state of the world, ask the LLM what to do next and return structured actions 
        """
        #Observe 
        screenshot_bytes = capture_and_optimize_screen()

        # 2. Build prompt 
        system_prompt = build_system_prompt()
        user_prompt = build_user_prompt(state)

        raw_output = call_llm(

            model = self.model , 
            system_prompt = system_prompt ,
            user_prompt = user_prompt ,
            image_bytes = screenshot_bytes
        )

        # 3. Parse LLM response
        try: 
            actions = self._parse_actions(raw_output)
            return actions
        except Exception as e:
            raise RuntimeError(f"Decider failed : {e}")

    # def _parse_actions(self, raw_output: str) -> List[Action]:
    #     """
    #     Force LLM output into valid Action objects.
    #     """

    #     try:
    #         cleaned = self._clean_json(raw_output)
    #         data = json.loads(cleaned)

    #         if not isinstance(data, list):
    #             raise ValueError("Expected list of actions")

    #         return [Action.from_dict(a) for a in data]

    #     except Exception as e:
    #         raise RuntimeError(f"Invalid LLM output: {e}")
        
    # def _clean_json(self, text: str) -> str:
    #     text = text.strip()

    #     if text.startswith("```"):
    #         text = text.split("```")[1]

    #     if text.endswith("```"):
    #         text = text.rsplit("```", 1)[0]

    #     return text.strip()

    def _parse_actions(self, raw_output: str):
        print("\n[DEBUG] Raw LLM output:\n", raw_output)

        extracted = extract_json(raw_output)
        print("\n[DEBUG] Extracted JSON:\n", extracted)

        data = json.loads(extracted)

        if not isinstance(data, dict):
            raise RuntimeError("Top-level JSON must be an object")

        if "actions" not in data:
            raise RuntimeError("Missing 'actions' field in JSON")

        actions = data["actions"]

        if not isinstance(actions, list):
            raise RuntimeError("'actions' must be a list")

        parsed_actions = []

        for i, a in enumerate(actions):
            if not isinstance(a, dict):
                raise RuntimeError(f"Action {i} is not an object")

            if "type" not in a:
                raise RuntimeError(f"Action {i} missing 'type'")

            parsed_actions.append(
                Action(
                    action_type=a["type"],
                    **{k: v for k, v in a.items() if k != "type"}
                )
            )

        return parsed_actions



import base64
from openai import OpenAI

client = OpenAI()

def call_llm(
    system_prompt: str,
    user_prompt: str,
    image_bytes: bytes,
    model: str = "gpt-4o"
) -> str:
    """
    Sends system + user prompt and a screenshot to the LLM.
    Returns raw text output.
    """

    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": user_prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                }
            ]
        }
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )

    return response.choices[0].message.content
