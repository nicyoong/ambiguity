import ambiguity
import amconfig
import json
import sys


def run_demo():
    client = amconfig._client()

    # Edit freely:
    # samples = [
    #     "I saw the man with the telescope.",
    #     "Every student didn’t submit the assignment.",
    #     "Alex told Jordan that they were late.",
    #     "The chicken is ready to eat.",
    #     "She can’t recommend the book too highly.",
    #     "A reviewer might reject every paper.",
    #     "The students seem ready to leave.",
    #     "Maria scolded Elena. This upset her.",
    # ]

    samples = [
        "I don’t think every reviewer who looked at the paper would necessarily recommend rejecting it.",
        "Jordan emailed Alex after the meeting. They said the decision was unfair and that it might need to be revisited.",
        "I’m not sure it would be appropriate to say that everyone was unhappy with how the feedback was handled.",
        "I don’t agree that everyone who raised concerns about the timeline was opposed to moving forward.",
        "The manager criticized the proposal during the call. That surprised her, even though she had expected some pushback.",
    ]

    for i, text in enumerate(samples, start=1):
        print(f"\n=== SAMPLE {i} ===")
        print(text)

        analysis = ambiguity.analyze_ambiguity(client, text, language_context="English", max_interpretations=6)
        analysis = ambiguity.normalize_analysis(client, analysis)

        print("\n--- Analysis (JSON) ---")
        print(json.dumps(analysis, ensure_ascii=False, indent=2))

