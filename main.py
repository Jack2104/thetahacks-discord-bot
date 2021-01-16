import os

import discord
from dotenv import load_dotenv

# The token is private, so this stops nasty people hijacking our stuff fom our public repo
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()


@client.event
async def on_ready():
    # The good stuff...
    pass

client.run(TOKEN)
