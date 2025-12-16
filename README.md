# Ambiguity Discord Bot

## Overview

This Discord bot analyzes linguistic ambiguity in sentences and short texts.
Rather than guessing the “correct” interpretation, it explicitly enumerates the distinct readings licensed by the language and explains why each reading is possible.

The bot treats ambiguity as:

- A structural property of language
- A product of syntax, semantics, and pragmatics
- Something to be analyzed, not resolved

Outputs are structured, inspectable, and theory-explicit.

## What this bot is not

- Not grammar correction

- Not paraphrasing for clarity

- Not disambiguation or ranking

- Not a meaning predictor

The bot does not decide which interpretation is intended.

## Commands

`/ambiguity`

Analyze a sentence or short paragraph for linguistic ambiguity.

## What it does

Given an input text, the bot:

1. Determines whether the text is ambiguous

2. Identifies the type(s) of ambiguity, such as:

- Structural (syntactic attachment)

- Scope (quantifiers, negation, modality)

- Referential (pronouns, deixis)

- Lexical (word-level meaning)

- Mixed (multiple interacting sources)

3. Enumerates distinct interpretations

4. Explains the specific linguistic trigger for each interpretation

All interpretations are treated as co-licensed, not competing.

## How to use

1. Type `/ambiguity`

2. Paste a sentence or short paragraph

3. (Optional) Set max_interpretations

4. Submit the command

Example input

`Everyone didn’t leave.`

## Output format

The bot returns one or more messages containing JSON output.

Key fields

- `input_text`
The analyzed text.

- `is_ambiguous`
true or false.

- `ambiguity_summary`
A brief explanation of why ambiguity is (or is not) present.

- `ambiguity_types`
A list of ambiguity categories involved.

- `interpretations`
Each interpretation includes:

A paraphrase

The ambiguity type

The exact trigger (text span + linguistic feature)

A clear explanation

`notes`
Additional observations or limits of inference.

## If the text is unambiguous

The output will:

- Set is_ambiguous to false

- Include exactly one interpretation

- Explain why alternative readings are not licensed

## Output length & formatting

- Outputs are automatically split across messages if long

- No interpretations are truncated

- JSON can be copy-pasted and recombined exactly