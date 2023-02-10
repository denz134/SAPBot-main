import discord
from discord import Embed
from discord.commands import Option, slash_command
from discord.ext import commands
from functions import *

class Roles(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @slash_command(guild_ids=guild_ids, name="promote", description="Promotes the specified user in the guild")
    @commands.has_permissions(ban_members=True)
    async def _promote(self, ctx, username: Option(str, "The Roblox username of the person you wish to promote", required=True)):
        user_id, name = get_user_id_from_name(username)
        if user_id == "NO_SUCH_USER":
        	await ctx.respond('Could not find a user with the name: "{username}"')
        result, roleObj = promote(user_id)
        if result == "SUCCESS":
        	successEmbed = discord.Embed(title="Successfully promoted **{}** to **{}**".format(name, roleObj["name"]), description="**{}** (ID: {}) has successfully been promoted to the role: **{}** (ID: {})".format(name, user_id, roleObj["name"], roleObj["roleId"]), color=discord.Colour.green())
        	successEmbed.set_thumbnail(url=get_roblox_avatar(user_id))
        	await ctx.respond(embed=successEmbed)
        elif result == "MAX":
        	await ctx.respond("The user is already at the highest possible role!")
        elif result == "NOT_IN_GROUP":
        	await ctx.respond("Doesn't look like the user has joined the group.")
        else:
        	await ctx.respond("An unexpected error occurred.")

    @slash_command(guild_ids=guild_ids, name="demote", description="demote the specified user in the guild")
    @commands.has_permissions(ban_members=True)
    async def _demote(self, ctx, username: Option(str, "The Roblox username of the person you wish to demote", required=True)):
        user_id, name = get_user_id_from_name(username)
        if user_id == "NO_SUCH_USER":
        	await ctx.respond("Could not find a user with the name: **{}**".format(username))
        result, roleObj = demote(user_id)
        if result == "SUCCESS":
        	successEmbed = discord.Embed(title="Successfully demoted **{}** to **{}**".format(name, roleObj["name"]), description="**{}** (ID: {}) has successfully been demoted to the role: **{}** (ID: {})".format(name, user_id, roleObj["name"], roleObj["roleId"]), color=discord.Colour.green())
        	successEmbed.set_thumbnail(url=get_roblox_avatar(user_id))
        	await ctx.respond(embed=successEmbed)
        elif result == "MAX":
        	await ctx.respond("The user is already at the highest possible role!")
        elif result == "NOT_IN_GROUP":
        	await ctx.respond("Doesn't look like the user has joined the group.")
        else:
        	await ctx.respond("An unexpected error occurred.")

    @slash_command(guild_ids=guild_ids, name="setrole", description="Set's the role of the specified user to the specified role")
    @commands.has_permissions(ban_members=True)
    async def _setrole(self, ctx, username: Option(str, "The Roblox username of the person you wish to demote", required=True), role_name: Option(str, "The role you wish to set the user's role to", required=True)):
        user_id, name = get_user_id_from_name(username)
        if user_id == "NO_SUCH_USER":
        	await ctx.respond("Could not find a user with the name: **{}**".format(username))
        role_id, roleName = get_role_id_from_name(role_name)
        set_role(user_id, role_id)
        successEmbed = discord.Embed(title="Successfully set **{}**\'s role to **{}**".format(name, roleName), description="**{}** (ID: {}) role has been successfully changed to : **{}** (ID: {})".format(name, user_id, roleName, role_id), color=discord.Colour.green())
        successEmbed.set_thumbnail(url=get_roblox_avatar(user_id))
        await ctx.respond(embed=successEmbed)

    @slash_command(guild_ids=guild_ids, name="robloxban", description="Bans the specified specified user in the roblox game")
    @commands.has_permissions(ban_members=True)
    async def _robloxban(self, ctx, username: Option(str, "The Roblox username of the person you wish to demote", required=True), reason: Option(str, "The reason for the ban", required=True), evidence: Option(str, "A URL to the video/image of evidence for this ban", required=True), duration: Option(str, "The duration of the ban. (1h, 1d, 1w, 1mo, 1yr)", required=True)):
    	user_id, actualName = get_user_id_from_name(username)
    	await ctx.respond("Give me a moment.. ")
    	if user_id == "NO_SUCH_USER":
    		await ctx.send("I couldn't find such a user!")
    	creationResult = create_ban_card(user_id, reason, evidence, duration)
    	if creationResult == "INVALID_USERID":
    		await ctx.send("I couldn't find such a user!")
    	elif creationResult == "ALREADY_BANNED":
    		await ctx.send("That person is already banned! Use `/records {}` for information".format(actualName))    		
    	else:
	    	descString = creationResult["desc"]
	    	roblox_avatar = get_roblox_avatar(user_Id)
	    	bannedEmbed = discord.Embed(title=f"Successfully banned **{actualName}** (ID: {user_id})", description=descString, color=discord.Colour.green())
	    	bannedEmbed.set_thumbnail(roblox_avatar)
	    	await ctx.send(embed=bannedEmbed)
		
    @_robloxban.error			
    async def error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("You don't have permission to do that!", ephemeral=True)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.respond("I don't have permission to do that!", ephemeral=True)
	
    @_promote.error			
    async def error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("You don't have permission to do that!", ephemeral=True)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.respond("I don't have permission to do that!", ephemeral=True)

    @_demote.error			
    async def error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("You don't have permission to do that!", ephemeral=True)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.respond("I don't have permission to do that!", ephemeral=True)
	
    @_setrole.error			
    async def error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("You don't have permission to do that!", ephemeral=True)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.respond("I don't have permission to do that!", ephemeral=True)


def setup(client):
    client.add_cog(Roles(client))
