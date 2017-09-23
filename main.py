"""main.py is the executing file which starts the bot & then loads the cogs."""
import discord
from config import *
# Import utils logging functions
from utils import log

client = discord.Client()

log("Connecting to Discord...", "init")

@client.event
async def on_ready():
    """Function call for when the bot is initialized."""

    log(f'Successfully logged in as {client.user}.', "on_ready()")


client.run(f'{config["discord_token"]}')
