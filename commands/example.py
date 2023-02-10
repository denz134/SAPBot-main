"""
Heya, this was made by Crypted.
You can use this code to make your own commands. 
I've left comments in the code to help you get an understanding of what it is and what it does.
Just to note: The module used here is NOT discord.py. It's a new maintained module called Pycord.
Here are the docs for it: https://docs.pycord.dev/.
Contact Crypted if you encounter any issues.

https://discord.com/users/657210542938914816

"""

# These lines are for importing necessary modules related to Discord.
import discord
from discord.commands import Option, slash_command
from discord.ext import commands
from discord.ext.commands.context import Context

from functions import * # This imports every function and variable from our functions.py file

# This is the class that will be used to create your commands.
class ExampleCommand(commands.Cog):
    def __init__(self, client): # The init function runs when the command is loaded.
        self.client = client # This is so that we can use functions of our client object in this class.

    @slash_command(guild_ids=guild_ids, name="mention", description="ping someone!") # This is a slash command. The Guild IDs needs to be your server IDs. It can be made global but it might take hours to get registered. Leave guild ids empty for it to be global. Note that by default it is set to the array "guild_ids" from the functions.py file
    async def mention(self, ctx, OptionOne: Option(discord.Member, description="The user you want to ping")): # This function runs when the command is called
        await ctx.respond(discord.Member) # This returns a response to the slash command. All slash commands must have a resopnse or else it would display "This interaction has failed" on Discord.
        """
        Tip, if you want the message to be visible to just the author, with the "Only you can see this message" text, just do this:
        await ctx.respond("Blah Blah", ephemeral=True)
        """

    @mention.error # This is a decorator. It runs when the command fails.
    async def ping_error(self, ctx: Context, error): # This function runs when the command fails.
        await ctx.respond(error, ephemeral=True) # This shows the error to the user 
        raise error # Logs the error to the console.

# This function is used to tell our client that this class is a cog.
def setup(client):
    client.add_cog(ExampleCommand(client))

# And voila, that's the command!
