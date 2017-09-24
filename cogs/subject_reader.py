"""
Subject reader cog

This cog enables users to inform the bot of what subjects they're doing, which
allows the bot to respond by adding the appropriate roles.
Subject data is given by issuing a command to the bot, rather than trying to
analyze message data.
"""
# Import utils for finding roles
from discord import utils
from discord.ext import commands
# Levenshtein module for fuzzy search
from Levenshtein import distance as lev_dist
# Logging
from utils import log

"""
Configuration:

MAX_FUZZY_DIST -- the maximum distance at which the best match will still be
considered a match (so that total gibberish isn't counted as a subject)
BASE_SUBJECTS -- all subjects which have an 'actual lesson',
i.e. ones that count towards your four.
SUBJECTS -- an array of all restricted rooms (except Year rooms)
ROLES -- a dict with keys being the entries in SUBJECTS and values being the
corresponding roles
"""

MAX_FUZZY_DIST = 4

BASE_SUBJECTS = [
    "Art",
    "Biology",
    "Business",
    "Chemistry",
    "Computer Science",
    "Drama",
    "Economics",
    "Engineering",
    "English",
    "French",
    "Film & Media",
    "Further Maths",
    "Geography",
    "German",
    "History",
    "ICT",
    "Maths",
    "Music",
    "Philosophy",
    "Physics",
    "Politics",
    "Product Design",
    "Psychology",
    "Sociology",
    "Spanish",
]

SUBJECTS = BASE_SUBJECTS + ["EPQ", "CIE", "Weeb"]

ROLES = {

}

class SubjectReader:
    """
    Command class for all subject-related commands.

    Includes:
    #addsubject
    #dropsubject
    #changesubject
    """

    def __init__(self, bot):
        self.bot = bot

        # We need to get a server object for the SF discord to search its roles
        self.guild = bot.get_guild(361492994144206849)

        # Populate the role dictionary by pre-fetching roles
        for subject in SUBJECTS:
            subject_role = utils.find(lambda r, n=subject: r.name == n, self.guild.roles)

            # Error message for 'not found', but we'll add None to the dictionary anyway.
            # If a user tries to add a subject for which there isn't a role, that will
            # be handled.
            if subject_role is None:
                log(f"Could not get role for subject {subject}. " +
                    "Please ensure that a role of this name exists.",
                    "SubjectReader __init___()", "error")

            ROLES[subject] = subject_role

    @commands.command(name="addsubject")
    @commands.guild_only()
    async def add_subject(self, ctx, *, subject: str):
        """
        Command handler for #addsubject. Adds a subject to a user.

        Arguments:
        subject -- a string representation of a subject name, which is used as
        a query for a fuzzy search to find the appropriate role.
        """

        # Get role using fuzzy search based on argument
        role_name = self.subject_fuzzy_search(subject)
        # If they typed in gibberish and there's no actual subject
        if role_name is None:
            await ctx.message.add_reaction("👎")
            return

        role = ROLES[role_name]
        # Same as before, except if it's a subject but there's no role
        # This is an admin config issue, so it deserves more than a thumbs down.
        if role is None:
            log(f"User tried to add subject {role_name} for which there was no role.",
                "add_subject()", "error")
            await ctx.send("The subject you entered was valid, but there is no role for it yet.")
            return

        # Once we have a role, add it if they don't already have 5.
        if self.count_current_subjects(ctx.message.author) >= 5:
            await ctx.message.add_reaction("🤔")
            await ctx.send("Doing more than five subjects is quite rare. Please " +
                           "speak to a member of the mod team to override.")
            return

        # Add
        await ctx.message.author.add_roles(role)
        await ctx.message.add_reaction("👍")

    @staticmethod
    def subject_fuzzy_search(subject):
        """
        Fuzzy searches the constant array SUBJECTS to find the closest match to
        the parameter subject, and then returns it.

        Arguments:
        subject -- a query for the fuzzy search.
        """
        # The fuzzy search is performed by iterating through the array and working out
        # the subject with the least edit distance. 

        # Special case: lowercase 'epq' has the same edit distance to EPQ as it does to CIE or Art.
        if subject == "epq":
            return "EPQ"

        # This for loop finds the match with the minimum distance
        minimum_distance = -1
        current_match = ""
        for known_subject in SUBJECTS:
            distance = lev_dist(subject, known_subject)
            if distance < minimum_distance or minimum_distance == -1:
                # If new record
                minimum_distance = distance
                current_match = known_subject

        # Ensure that match is suitable
        if minimum_distance < MAX_FUZZY_DIST:
            return current_match

    @staticmethod
    def count_current_subjects(member):
        """
        Count the number of subject roles the user already has.
        Used for enforcing a limit of 5 subject roles, unless manually overridden
        by a moderator.

        Arguments:
        member -- the member to get the subject role count for.
        """
        # Return the length of the list which contains the intersections between
        # their list of role namesand the BASE_SUBJECTS list, so we aren't counting
        # EPQ or CIE
        return len(
            list(set((role.name for role in member.roles)).intersection(BASE_SUBJECTS))
        )

def setup(bot):
    """ Add the cog to the bot """
    bot.add_cog(SubjectReader(bot))