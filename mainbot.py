from __future__ import annotations

import json
import asyncio
import os
import discord
from discord import app_commands

import amconfig
import amutils
import ambiguity


TOKEN = os.environ["BOT_TOKEN"]

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

analysis_lock = asyncio.Lock()

def split_message(text: str, limit: int = 1900):
    chunks = []
    while text:
        chunks.append(text[:limit])
        text = text[limit:]
    return chunks


async def send_json_chunks(interaction: discord.Interaction, payload: dict):
    output = json.dumps(payload, ensure_ascii=False, indent=2)
    chunks = split_message(output)

    total = len(chunks)
    for i, chunk in enumerate(chunks, start=1):
        await interaction.followup.send(
            f"**Part {i}/{total}**\n```json\n{chunk}\n```"
        )

@tree.command(
    name="ambiguity",
    description="Analyze linguistic ambiguity in a sentence or short paragraph"
)
@app_commands.describe(
    text="Sentence or short paragraph to analyze",
    max_interpretations="Maximum number of interpretations (default: 6)"
)
async def ambiguity_command(
    interaction: discord.Interaction,
    text: str,
    max_interpretations: int = 6,
):
    await interaction.response.defer(thinking=True)

    async with analysis_lock:
        client_llm = amconfig._client()

        analysis = await asyncio.to_thread(
            ambiguity.analyze_ambiguity,
            client_llm,
            text,
            "English",
            max_interpretations
        )

    await send_json_chunks(interaction, analysis)

@tree.command(
    name="ambiguity_normalize",
    description="Normalize and deduplicate an ambiguity analysis JSON"
)
@app_commands.describe(
    analysis_json="Raw ambiguity analysis JSON (paste full JSON)"
)
async def ambiguity_normalize_command(
    interaction: discord.Interaction,
    analysis_json: str,
):
    await interaction.response.defer(thinking=True)

    try:
        analysis = json.loads(analysis_json)
    except json.JSONDecodeError:
        await interaction.followup.send("❌ Invalid JSON input.")
        return

    async with analysis_lock:
        client_llm = amconfig._client()

        normalized = await asyncio.to_thread(
            ambiguity.normalize_analysis,
            client_llm,
            analysis
        )

    await send_json_chunks(interaction, normalized)

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}")

client.run(TOKEN)
