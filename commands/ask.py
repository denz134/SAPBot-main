import discord
from discord import Embed
from discord.commands import Option, slash_command
from discord.ext import commands
from functions import *

class Ask(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @slash_command(guild_ids=guild_ids, name="ask", description="Answers your question")
    async def _joke(self, ctx, question: Option(str, "The question you want to ask me", required=False)):
        responses = [
            "It is certain.",
            "My sources say no.",
            "Don't count on it.",
            "Outlook not so good.",
            "It is decidedly so.",
            "Better not tell you now.",
            "Very doubtful.",
            "Yes - definitely.", 
            "Just no.", 
            "Please don't",
            "Ask again later. Totally not random.",
        ]
        if question == None:
            await ctx.respond(random.choice(responses))
        else:
            await ctx.respond("{}\n\n **{}**".format(question, random.choice(responses)))
        
def setup(client):
    client.add_cog(Ask(client))
