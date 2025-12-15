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

def _try_parse_json(text: str) -> Optional[Dict[str, Any]]:
    """
    Attempts to parse JSON from model output.
    Strips Markdown backticks and tries to extract a JSON object.
    """
    if not text:
        return None

    cleaned = text.strip()
    cleaned = cleaned.replace("```json", "").replace("```", "").replace("`", "").strip()

    candidate = _extract_json_object(cleaned) or cleaned
    try:
        return json.loads(candidate)
    except Exception:
        return None

