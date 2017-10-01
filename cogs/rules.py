"""
Rules cog

This cog provides the ability to post an embed of all the rules of the server.
"""

from discord.ext import commands
from config import config
from discord import Colour, Embed

class Rules:
    """
    Class to contain all the relevant handlers in this cog for the
    commands listed above.

    Includes the commands:
    #postrules
    """

    def __init__(self, bot):
        self.bot = bot
        # Pre-define rules embed
        self.rules_embed = Embed(title="Rules", type="rich", colour=Colour.red())
        # Populate
        for rule, explanation in config["rules"].items():
            self.rules_embed.add_field(name=rule, value=explanation, inline=False)

    @commands.command(name="postrules", hidden=True)
    @commands.is_owner()
    async def post_rules(self, ctx):
        """ Post the rules embed in the current channel. """
        await ctx.send(embed=self.rules_embed)

def setup(bot):
    """ Add the cog to the bot """
    bot.add_cog(Rules(bot))
