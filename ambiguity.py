from __future__ import annotations

import json
from openai import OpenAI
from typing import Any, Dict

import amconfig
import amutils


# Step 1: ambiguity analysis
def analyze_ambiguity(
    client: OpenAI,
    text: str,
    language_context: str = "English",
    max_interpretations: int = 6,
) -> Dict[str, Any]:
    system = "You are a linguistics expert specializing in semantics, syntax, and pragmatics. You detect and explain ambiguity."
    user = f"""
{amconfig.AMBIGUITY_GUIDE}

Analyze the following input for linguistic ambiguity.

Context:
- Language context: {language_context}
- Input may be a sentence or short paragraph; keep interpretations at the level of the whole input.

Input:
\"\"\"{text}\"\"\"

Return ONLY a JSON object with this exact shape:

{{
  "input_text": "string",
  "is_ambiguous": true,
  "ambiguity_summary": "string",
  "ambiguity_types": [
    {{
      "type": "structural|scope|referential|lexical|mixed",
      "description": "string"
    }}
  ],
  "interpretations": [
    {{
      "id": "I1",
      "paraphrase": "string",
      "ambiguity_type": "structural|scope|referential|lexical",
      "trigger": {{
        "text_span": "string",
        "linguistic_feature": "string"
      }},
      "explanation": "string"
    }}
  ],
  "notes": ["string"]
}}

Constraints:
- If unambiguous:
  - set "is_ambiguous": false
  - "ambiguity_types" must be []
  - "interpretations" must contain exactly ONE interpretation (I1) that restates the meaning.
  - "ambiguity_summary" should say why multiple readings are not licensed.
- If ambiguous:
  - Provide at most {max_interpretations} interpretations.
  - Interpretations must be genuinely distinct (not minor rewordings).
  - Do NOT rank interpretations by likelihood.
  - Each interpretation must be tied to a specific trigger and linguistic feature.
- Do NOT provide grammar correction.
"""
    return amutils.llm_json(client, system=system, user=user, temperature=0.2)

# Step 2 (optional): normalize/dedupe interpretations
def normalize_analysis(
    client: OpenAI,
    analysis: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Second pass to:
    - remove near-duplicate interpretations
    - ensure IDs are sequential (I1..In)
    - ensure types adhere to allowed labels
    - keep content descriptive, not judgmental

    This is helpful for demo polish and stability.
    """
    system = "You are a careful JSON editor and linguistics analyst. You fix structure and deduplicate interpretations without changing meaning."
    user = f"""
You will receive a JSON analysis output. Your job:
- Keep the same overall schema and keys.
- Remove duplicate/overlapping interpretations (merge if needed).
- Ensure each interpretation is genuinely distinct.
- Ensure IDs are sequential: I1, I2, ...
- Ensure "ambiguity_types" is consistent with interpretations.
- Do NOT add new interpretations unless required to fix a missing obvious reading already implied by the analysis.
- Do NOT add judgmental language. Do NOT do grammar correction.

Here is the JSON to normalize:
{json.dumps(analysis, ensure_ascii=False, indent=2)}

Return ONLY the corrected JSON object.
"""
    return amutils.llm_json(client, system=system, user=user, temperature=0.1)
