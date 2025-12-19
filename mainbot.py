from __future__ import annotations

import json
import asyncio
import os
import discord
from discord import app_commands
from discord.ext import commands

import amconfig
import amutils
import ambiguity


TOKEN = os.environ["BOT_TOKEN"]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix="a!",
    intents=intents
)
tree = bot.tree
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

async def run_ambiguity(text: str, max_interpretations: int):
    client_llm = amconfig._client()

    return await asyncio.to_thread(
        ambiguity.analyze_ambiguity,
        client_llm,
        text,
        "English",
        max_interpretations
    )


async def run_ambiguity_normalize(analysis: dict):
    client_llm = amconfig._client()

    return await asyncio.to_thread(
        ambiguity.normalize_analysis,
        client_llm,
        analysis
    )

@tree.command(
    name="ambiguity",
    description="Analyze linguistic ambiguity in a sentence or short paragraph"
)
@app_commands.describe(
    text="Sentence or short paragraph to analyze",
    max_interpretations="Maximum number of interpretations (default: 6)"
)
async def ambiguity_slash(
    interaction: discord.Interaction,
    text: str,
    max_interpretations: int = 6,
):
    await interaction.response.defer(thinking=True)

    async with analysis_lock:
        analysis = await run_ambiguity(text, max_interpretations)

    await send_json_chunks(interaction, analysis)

@bot.command(name="ambiguity")
async def ambiguity_prefix(
    ctx: commands.Context,
    *,
    text: str
):
    async with ctx.typing():
        async with analysis_lock:
            analysis = await run_ambiguity(text, max_interpretations=6)

    output = json.dumps(analysis, ensure_ascii=False, indent=2)
    for i, chunk in enumerate(split_message(output), start=1):
        await ctx.send(f"**Part {i}**\n```json\n{chunk}\n```")

@tree.command(
    name="ambiguity_normalize",
    description="Normalize and deduplicate an ambiguity analysis JSON"
)
@app_commands.describe(
    analysis_json="Raw ambiguity analysis JSON (paste full JSON)"
)
async def ambiguity_normalize_slash(
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
        normalized = await run_ambiguity_normalize(analysis)

    await send_json_chunks(interaction, normalized)

@bot.event
async def on_ready():
    asyncio.create_task(amutils.checktime())
    await tree.sync()
    print(f"Logged in as {bot.user}")

bot.run(TOKEN)
