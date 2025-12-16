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