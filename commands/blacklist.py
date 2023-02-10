import discord
from discord import Embed
from discord.commands import Option, slash_command
from discord.ext import commands
from functions import *

class Blacklist(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @slash_command(guild_ids=guild_ids, name="blacklist", description="Blacklist someone from all the servers")
    @commands.has_permissions(ban_members=True)
    async def _blacklist(self, ctx, user: Option(discord.User, description="The user to blacklist from all the servers", required=True), reason: Option(str, description="The reason for the blacklist", required=False)):
        if reason == None:
            reason = "Reason Unspecified"
        theString = ", \n".join(guild.name for guild in self.client.guilds)
        print(theString)
        try:
            userEmbed = Embed(title="You have been blacklisted", description=f"You have been blacklisted from the following servers: \n{serverString}", color=0xFF0000)
            userEmbed.add_field(name="Reason", value=reason)
            await user.send(embed=userEmbed)
            await ctx.respond(embed=userEmbed)
        except:
            pass
        for guild in self.client.guilds:
            guildMember = await guild.fetch_member(user.id)
            await guild.ban(guildMember, reason="Blacklisted: Reason: {}".format(reason))
        await ctx.respond("Blacklisted {}".format(guildMember))

    @_blacklist.error
    async def error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("You don't have permission to do that!", ephemeral=True)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.respond("I don't have permission to do that!", ephemeral=True)

def setup(client):
    client.add_cog(Blacklist(client))
