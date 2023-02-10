import discord
from discord import Embed
from discord.commands import Option, slash_command
from discord.ext import commands
from functions import *

class Meme(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @slash_command(guild_ids=guild_ids, name="meme", description="Sends a random meme")
    async def _joke(self, ctx):
        memeEmbed = getMemeEmbed()
        await ctx.respond(embed=memeEmbed)
        
def setup(client):
    client.add_cog(Meme(client))
