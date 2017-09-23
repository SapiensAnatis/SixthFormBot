"""main.py is the executing file which starts the bot & then loads the cogs."""
import discord
from discord.ext import commands
# Import config dict
from config import config
# Import utils logging functions
from utils import log

initial_extensions = ["cogs.subject_reader"]
bot = commands.Bot(command_prefix="~", description="Sixth form bot")

log("Connecting to Discord...", "init")

@bot.event
async def on_ready():
    """Function call for when the bot is initialized."""

    log(f"Successfully logged in as {bot.user}.", "on_ready()")
    log(f"Loading modules...", "on_ready()")
    # Load cogs
    if __name__ == "__main__":
        for extension in initial_extensions:
            try:
                print(f"\t{extension[5:]}...", end="")
                bot.load_extension(extension)
                print("done!")
            except ImportError:
                log(f"\nCould not find cog {extension}. Check that it exists.", "on_ready()", "error")
            except discord.ClientException:
                log(f"\nCog {extension} was invalid (no setup func).", "on_ready()", "error")

    log(f"Module loading complete.", "on_ready()")

bot.run(f'{config["discord_token"]}', bot=True, reconnect=True)
