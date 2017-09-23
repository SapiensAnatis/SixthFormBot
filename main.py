import discord
# Import utils logging functions, for logging, and path functions to retrieve bot token
from utils import log, localize_filepath

client = discord.Client()

log("Connecting to Discord...", "init")

# Called when the bot is fully initialized.
@client.event
async def on_ready():
    log(f'Successfully logged in as {client.user}.', "on_ready()")

# Function to get token on startup. Would rather not pollute global scope with these variables
def get_token():
    # Retrieve token to log in with
    token_filepath = localize_filepath("keychain/discord_token.txt")
    token_file = open(token_filepath)
    return token_file.read()

client.run(f'{get_token()}')