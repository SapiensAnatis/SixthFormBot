"""main.py is the executing file which starts the bot & then loads the cogs."""
import discord
from discord.ext import commands
# Import config dict
from config import config
# Import utils logging functions
from utils import log

INITIAL_EXTENSIONS = ["cogs.subject_reader", "cogs.select_year"]
bot = commands.Bot(command_prefix="~", description="Sixth form bot")

log("Connecting to Discord...", "init")

@bot.event
async def on_ready():
    """Function call for when the bot is initialized."""

    log(f"Successfully logged in as {bot.user}.", "on_ready()")
    log(f"Loading modules...", "on_ready()")
    # Load cogs
    if __name__ == "__main__":
        for extension in INITIAL_EXTENSIONS:
            try:
                print(f"\t{extension[5:]}...", end="")
                bot.load_extension(extension)
                print("done!")
            except ImportError:
                log(f"\nCould not find cog {extension}. Check that it exists.",
                    "on_ready()", "error")
            except discord.ClientException:
                log(f"\nCog {extension} was invalid (no setup func).", "on_ready()", "error")

    log(f"Module loading complete.", "on_ready()")

# For the below commands, all cogs are assumed to be in the cogs folder.
@bot.command()
@commands.is_owner()
async def unload(ctx, cog_name: str):
    """
    Unloads a cog.

    Arguments:
    cog_name -- name of cog to unload.
    """

    bot.unload_extension(f"cogs.{cog_name}")
    log(f"Successfully unloaded extension {cog_name}.", "unload()")
    await ctx.message.add_reaction("✅")

@bot.command()
@commands.is_owner()
async def load(ctx, cog_name: str):
    """
    Loads a cog.

    Arguments:
    cog_name -- name of cog to load.
    """

    bot.load_extension(f"cogs.{cog_name}")
    log(f"Successfully loaded extension {cog_name}.", "load()")
    await ctx.message.add_reaction("✅")

@bot.command()
@commands.is_owner()
async def reload(ctx, cog_name: str):
    """
    Reloads a cog.

    Arguments:
    cog_name -- name of cog to reload.
    """

    bot.unload_extension(f"cogs.{cog_name}")
    log(f"Successfully unloaded extension {cog_name}.", "reload()")
    bot.load_extension(f"cogs.{cog_name}")
    log(f"Successfully loaded extension {cog_name}.", "reload()")
    await ctx.message.add_reaction("✅")

bot.run(f'{config["discord_token"]}', bot=True, reconnect=True)
