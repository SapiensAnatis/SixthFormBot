"""
Help cog

This cog provides the help command as an embed, overriding the default
code block style.
"""

from discord.ext import commands
from discord import Embed, Colour

class Help:
    """
    Class to contain all relevant commands for the replacement #help command.

    Includes:
    #help
    """

    def __init__(self, bot):
        self.bot = bot
        # Pre-define help embed
        self.embed = Embed(
            title="Sixth Form bot: commands",
            type="rich",
            colour=Colour.blue(),
        )

        bot_commands = [command for command in self.bot.commands if not command.hidden]

        for command in bot_commands:
            self.embed.add_field(
                name=command.name,
                value=f"{command.brief}\nUsage: {command.usage}"
            )

    @commands.command(name="help")
    @commands.guild_only()
    async def help(self, ctx, *command: str):
        """
        Help command handler. Posts the command info embed.abs
        """
        await ctx.send(embed=self.embed)


def setup(bot):
    """ Add the cog to the bot """
    bot.add_cog(Help(bot))
