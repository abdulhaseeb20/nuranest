import re

def extract_week(input_text: str) -> int | None:
    """
    Looks for phrases like "I am 6 weeks pregnant" or "currently 20 weeks"
    """
    input_text = input_text.lower()
    match = re.search(r"(\d{1,2})\s*(weeks|week)\b", input_text)
    if match:
        return int(match.group(1))
    return None
