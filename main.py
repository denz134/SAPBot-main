import discord
import os
import sys
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

client = discord.Bot()

# Ready Event
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="with fellow cops"))
    print(f'Successfully logged in as {client.user}.')

@client.event
async def on_message(msg):
    if msg.author.bot:
        return
    args = msg.content.split(" ")
    if len(args) > 1:
        if args[0] == "$sudo":
            cmd = args[1].lower()
            if cmd == "reload":
                extension = args[2].lower()
                try:
                    client.unload_extension(f"commands.{extension}")
                    client.load_extension(f"commands.{extension}")
                    embed = discord.Embed(title="SUCCESS_EXTENSION_RELOADED", description=f"```\n$sudo {cmd} {extension}\n>> Extension \"{extension}\" has been reloaded.\n```", color=discord.Colour.green())
                    await msg.reply(embed=embed)
                except Exception as e :
                    raise(e)
                    embed = discord.Embed(title="ERROR_EXTENSION_NOT_LOADED", description=f"```\n$sudo {cmd} {extension}\n>> ERROR: Extension \"{extension}\" could not be found.\n```", color=discord.Colour.red())
                    await msg.reply(embed=embed)
            elif cmd == "disable":
                extension = args[2].lower()
                try:
                    client.unload_extension(f"commands.{extension}")
                    embed = discord.Embed(title="SUCCESS_EXTENSION_DISABLED", description=f"```\n$sudo {cmd} {extension}\n>> Extension \"{extension}\" has been disabled\n```", color=discord.Colour.green())
                    await msg.reply(embed=embed)
                except Exception as e:
                    embed = discord.Embed(title="ERROR_EXTENSION_NOT_LOADED", description=f"```\n$sudo {cmd} {extension}\n>> ERROR: Extension \"{extension}\" could not be found.\n```", color=discord.Colour.red())
                    await msg.reply(embed=embed)
            elif cmd == "enable":
                extension = args[2].lower()
                try:
                    client.load_extension(f"commands.{extension}")
                    embed = discord.Embed(title="SUCCESS_EXTENSION_ENABLED", description=f"```\n$sudo {cmd} {extension}\n>> Extension \"{extension}\" has been enabled\n```", color=discord.Colour.green())
                    await msg.reply(embed=embed)
                except Exception as e:
                    raise(e)
                    embed = discord.Embed(title="ERROR_EXTENSION_NOT_LOADED", description=f"```\n$sudo {cmd} {extension}\n>> ERROR: Extension \"{extension}\" could not be found.\n```", color=discord.Colour.red())
                    await msg.reply(embed=embed)

# Restart command
@client.slash_command(name="restart", description="Restarts the bot")
@commands.is_owner()
async def restart(ctx):
    await ctx.respond("Restarting...", ephemeral=True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@restart.error
async def restartError(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.respond("You do not have permission to use this command.", ephemeral=True)

# Loading in our commands.
for file in os.listdir("./commands"):
    if file.endswith(".py"):
        if f"commands.{file[:-3]}" != "commands.example":
            client.load_extension(f"commands.{file[:-3]}")

client.run(os.getenv("BOTTOKEN"))
