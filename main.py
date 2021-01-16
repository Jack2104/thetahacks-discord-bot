# TODO: add the bot to the sever (from the developer portal) so we can do stuff

import os

import discord
from dotenv import load_dotenv

# The token is private, so this stops nasty people hijacking our stuff fom our public repo
# TODO: add the .env to a .gitingnore so that it doesn't show up on source control (would require creating
# a local copy on everyone's computers though... I can't even bo bothered rn)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()


@client.event
async def on_ready():
    # The good stuff...
    pass

client.run(TOKEN)
