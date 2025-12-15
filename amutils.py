import amconfig
import json
from openai import OpenAI
from typing import Any, Dict, Optional


def _extract_json_object(text: str) -> Optional[str]:
    """
    Attempt to extract the first top-level JSON object from a model response.
    Useful when the model wraps JSON with extra text.
    """
    if not text:
        return None

    # Strip common markdown fences first
    cleaned = text.replace("```", "").replace("`", "").strip()

    # If response is already pure JSON object
    if cleaned.startswith("{") and cleaned.endswith("}"):
        return cleaned

    # Try to locate a JSON object by bracket matching
    start = cleaned.find("{")
    if start == -1:
        return None

    depth = 0
    for i in range(start, len(cleaned)):
        ch = cleaned[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return cleaned[start : i + 1]

    return None

