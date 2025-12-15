import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

MODEL = "openai/gpt-oss-20b:free"
BASE_URL = "https://openrouter.ai/api/v1"
AMBIGUITY_GUIDE = """
You are performing linguistic ambiguity analysis (NOT grammar correction).

Ambiguity types (use ONLY these labels):
- structural: Different phrase structures/attachments yield different meanings (e.g., PP attachment, coordination).
- scope: Different scope relations among operators (negation, quantifiers, modals, adverbs, "only", comparatives).
- referential: Anaphora/deixis/definite description allows multiple antecedents or referents (pronouns, "the X", ellipsis).
- lexical: A word/phrase has distinct senses or category ambiguities (polysemy, homonymy).
- mixed: More than one type interacts in a single ambiguity (use sparingly; still tag each interpretation with one main type).

Rules:
- Be explanatory and descriptive; do not judge the sentence or "correct" it.
- Only include interpretations that are grammatically licensed by the sentence as written.
- Do NOT rank interpretations by likelihood.
- If the text is unambiguous, explain why only one coherent interpretation is available.
- If discourse context is needed to resolve a referent, state that in notes without inventing context.
- Only enumerate interpretations that are grammatically licensed by the surface form; do not posit silent syntactic constructions.
"""
