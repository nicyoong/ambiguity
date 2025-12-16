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