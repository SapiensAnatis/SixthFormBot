# /r/6thform Discord Bot

This bot is made for the /r/6thform Discord server and in future could replace moderators in handling subject/year roles, as well as perform a variety of other useful tasks.

## Setup
This bot is not intended to be self-hosted as it is specifically made for one Discord server. However, if you just want to learn from it or want to contribute, it will help to be able to run a local instance.

Create a file called `config.py`. This is a dictionary which provides several values essential to the operation of the bot. Here is the intended structure:
```python 
config = {
    "discord_token": "" # The token of the bot account on which the script will run.
    "guild_id": # As an int, the id of the server that the bot should operate on.
    "rules": {
        # A dict of rules to add to the embed given by #rules. Keys = titles, values = ..values
        "rule title": "rule description",
        "rule title 2": "rule description 2"
    }
}
```