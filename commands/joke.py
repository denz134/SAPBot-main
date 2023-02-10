import discord
from discord import Embed
from discord.commands import Option, slash_command
from discord.ext import commands
from functions import *

class Joke(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @slash_command(guild_ids=guild_ids, name="joke", description="Sends a random joke")
    async def _joke(self, ctx, type: Option(str, "The type of joke you want to see", choices=["Pun", "Programming", "Dark", "Misc", "Spooky", "Christmas"], required=False)):
        jokeEmbed = get_jokeEmbed(type)
        await ctx.respond(embed=jokeEmbed)
        
def setup(client):
    client.add_cog(Joke(client))
