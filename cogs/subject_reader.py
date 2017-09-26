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

        author = ctx.message.author

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

        # Check they don't already have five.
        if self.count_current_subjects(author) >= 5:
            await ctx.message.add_reaction("🤔")
            await ctx.send("Doing more than five subjects is quite rare. Please " +
                           "speak to a member of the mod team to override.")
            return

        # Check they don't already do it.
        if self.user_does_subject(author, role_name):
            await ctx.message.add_reaction("🤔")
            await ctx.send("You already have the role for that subject.")
            return

        await author.add_roles(role, reason="User added subject via addsubject command")
        await ctx.message.add_reaction("👍")

    @commands.command(name="dropsubject")
    @commands.guild_only()
    async def drop_subject(self, ctx, *, subject: str):
        """
        Command handler for #dropsubject. Removes a subject from a user.

        Arguments:
        subject -- a string representation of a subject name, which is used as
        a query for a fuzzy search to find the appropriate role.
        """

        # Save typing
        author = ctx.message.author

        # Get role using fuzzy search based on argument
        role_name = self.subject_fuzzy_search(subject)
        # If they typed in gibberish and there's no actual subject
        if role_name is None:
            await ctx.message.add_reaction("👎")
            return

        role = ROLES[role_name]

        # Check they actually do it.
        # I could just attempt to remove it and handle the error, but that's
        # extra API calls
        if not self.user_does_subject(author, role_name):
            await ctx.message.add_reaction("🤔")
            await ctx.send("You don't do that subject.")
            return

        # Ensure that they're not going down to two subjects (most do three in the end)
        if self.count_current_subjects(author) < 3:
            await ctx.message.add_reaction("🤔")
            await ctx.send("Doing less than three subjects is quite rare. Please " +
                           "speak to a member of the mod team to override.")
            return

        await author.remove_roles(role, reason="User dropped subject via dropsubject command")
        await ctx.message.add_reaction("👍")

    @commands.command(name="changesubject")
    @commands.guild_only()
    async def change_subject(self, ctx, *, args):
        """
        Command handler for #changesubject. Changes one subject to another.

        Arguments:
        args -- two subjects seperated by a comma, with the one on the left being
        the original subject, and the one on the right the new one.
        e.g. "#changesubject history, sociology": changes history to sociology
        """
        author = ctx.message.author

        # Get our two subjects by splitting them into a list w/o whitespace:
        subjects = [subject.strip() for subject in args.split(",")]
        # Check they did it properly
        if len(subjects) < 2:
            await ctx.send("Please give a subject you want to change, what to, split by a comma.")
            return
        elif len(subjects) > 2:
            await ctx.send("This command only supports the ability to change one subject at once.")
            return

        # Perform lookup
        first_subject = self.subject_fuzzy_search(subjects[0])
        second_subject = self.subject_fuzzy_search(subjects[1])

        if first_subject is None or second_subject is None:
            await ctx.message.add_reaction("👎")
            return

        # Check that they actually do the first subject
        if not self.user_does_subject(author, first_subject):
            await ctx.send("Please put a subject that you currently do on the left side.")
            return

        await author.remove_roles(SUBJECTS[first_subject], reason="User dropped subject via changesubject command")
        await author.add_roles(SUBJECTS[second_subject], reason="User added subject via changesubject command")
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
        # their list of role names and the BASE_SUBJECTS list, so we aren't counting
        # EPQ or CIE
        return len(
            list(set((role.name for role in member.roles)).intersection(BASE_SUBJECTS))
        )

    @staticmethod
    def user_does_subject(member, subject):
        """
        Return true/false if a user has the role for a subject or not.

        Arguments:
        member -- the member who may or may not be doing the subject
        subject -- string representation of the subject name, must be in SUBJECTS
        """
        return utils.find(lambda r, n=subject: r.name == n, member.roles) is not None

def setup(bot):
    """ Add the cog to the bot """
    bot.add_cog(SubjectReader(bot))
