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


tests = [
    '{"actions":[{"type":"done","summary":"ok"}]}',
    '```json\n{"actions":[{"type":"done","summary":"ok"}]}\n```',
    'Sure! Here you go:\n{"actions":[{"type":"write","text":"Hello"}]}',
    '',
    'No JSON here'
]

for t in tests:
    try:
        print(extract_json(t))
    except Exception as e:
        print("ERROR:", e)
