"""
Subject reader cog

This cog enables users to inform the bot of what subjects they're doing, which
allows the bot to respond by adding the appropriate roles.
Subject data is given by issuing a command to the bot, rather than trying to
analyze message data.
"""

import discord
from discord.ext import commands
# Levenshtein module for fuzzy search
from Levenshtein import distance as lev_dist
# Import config for max edit distance
from config import config

"""
Configuration:

MAX_FUZZY_DIST -- the maximum distance at which the best match will still be
considered a match (so that total gibberish isn't counted as a subject)
SUBJECTS -- an array of all restricted rooms (except Year rooms)
"""

MAX_FUZZY_DIST = 8

SUBJECTS = [
    "CIE",
    "Art",
    "Biology",
    "Business",
    "Chemistry",
    "Computer Science",
    "Drama",
    "Economics",
    "Engineering",
    "English",
    "EPQ",
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
    "Weeb"
]

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

    @commands.command(name="addsubject")
    @commands.guild_only()
    async def add_subject(self, ctx, *, subject: str):
        """
        Command handler for #addsubject. Adds a subject to a user.

        Arguments:
        subject -- a string representation of a subject name, which is used as
        a query for a fuzzy search to find the appropriate role.
        """

        actual_subject = self.subject_fuzzy_search(subject)
        await ctx.send(actual_subject or "Subject not found.")

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

        # This for loop finds the match with the minimum distance
        minimum_distance = -1
        current_match = ""
        for known_subject in SUBJECTS:
            distance = lev_dist(subject, known_subject)
            if distance < minimum_distance or minimum_distance == -1:
                # If new record
                minimum_distance = distance
                current_match = known_subject

        if minimum_distance < MAX_FUZZY_DIST:
            return current_match

def setup(bot):
    """ Add the cog to the bot """
    bot.add_cog(SubjectReader(bot))
