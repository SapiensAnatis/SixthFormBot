"""
Year selection cog

This cog enables users to get the role according to which
year they're in, again by entering a command.

I could've used reactions, but if we have a command for this then in theory the
#lobby chat can almost be eliminated.
"""

# Module imports
# Basic discord functionality
from discord.ext import commands
# Utils for find command
from discord import utils
# Config
from config import config

"""
Configuration:

YEARS -- a list of all the year role names.
ROLES -- a dictionary containing the Discord.Role objects. It is generated at
startup by searching for roles with the names in YEARS, and indexing them with
those names.

Roles are pre-fetched at startup to save the program from having to use
utils.find excessively every time a command is run. Effectively, roles are loaded
into memory to reduce read times.
"""

YEARS = ["Year 11", "Year 12", "Year 13"]
ROLES = {}

class SelectYear:
    """
    Extension class for the commands to define years.

    Includes:
    #setyear
    """

    def __init__(self, bot):
        self.bot = bot
        self.guild = bot.get_guild(config["guild_id"])

        # Populate role dict
        for year in YEARS:
            ROLES[year] = utils.find(lambda r, n=year: r.name == n, self.guild.roles)

    @commands.command(name="setyear")
    @commands.guild_only()
    async def set_year(self, ctx, *, year_argument: str):
        """
        Command handler for #setyear. Changes or initially defines
        the user's year role.

        Arguments:
        year_argument -- a string hopefully containing some indication
        as to what year the user wants to be in.
        """

        author = ctx.message.author

        # Fuzzy search the year role array to find which one's 'number'
        # is a substring of the argument.
        # e.g. we want year_role_name to be "Year 13" if "13" is in the argument.
        year_role_name = next((year for year in YEARS if year[5:] in year_argument), None)
        if year_role_name is None:
            await ctx.send("Please provide a valid year (words don't work).")
            return

        role = ROLES[year_role_name]
        existing_role = self.get_mem_year_role(author)

        # Checks
        # Skip checks if they don't already have a year role.
        if existing_role is not None:
            # Do they already have the role they're requesting?
            if role.name == existing_role.name:
                await ctx.send("You're already registered as being a part of that year group.")
                return

            await author.remove_roles(existing_role)

        # Add role, finally
        await author.add_roles(role)
        await ctx.message.add_reaction("👍")

    @staticmethod
    def get_mem_year_role(member):
        """
        Return the Discord.Role object for a member which is their Year role.
        In cases where a user has more than one, which shouldn't happen, the first
        one that discord.py happens to find is returned. If they don't have one,
        returns None.

        Arguments:
        member -- the Discord.Member object whose roles are being examined.
        """
        return utils.find(lambda r, l=YEARS: r.name in l, member.roles)


def setup(bot):
    """ Add the cog to the bot """
    bot.add_cog(SelectYear(bot))
