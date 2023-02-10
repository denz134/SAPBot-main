import discord
import youtube_dl
import asyncio
from discord import Embed
from discord.commands import Option, slash_command
from discord.ext import commands
from functions import *

queues = {}
ffmpeg_options = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}
ytdl_options = {"format":"bestaudio"}

ytdl = youtube_dl.YoutubeDL(ytdl_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('webpage_url')
        self.uploader = data.get('uploader')
        self.channel_url = data.get('channel_url')
        self.thumbnail = data.get('thumbnail')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False, play=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream or play))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = []

    @slash_command(guild_ids=guild_ids, name="leave", description="Leaves a VC")
    async def _leave(self, ctx):
        if ctx.voice_client is None:
            await ctx.respond("You're not in a VC!", ephemeral=True)
        else:
            await ctx.voice_client.disconnect()
        await ctx.respond("Bye!", ephemeral=True)

    def start_playing(self, ctx, player):
        self.queue.insert(0, player)
        i = 0
        while i <  len(self.queue):
            try:
                ctx.voice_client.play(self.queue[i], after=lambda e: print('Player error: %s' % e) if e else self.play_next(ctx, player))
            except:
                pass
            i += 1

    def play_next(self, ctx, before):
        self.queue.remove(before)
        print(self.queue)
        player = self.queue[len(self.queue) - 1]
        self.start_playing(ctx, player)

    @slash_command(guild_ids=guild_ids, name="play", description="Plays a song")
    async def _play(self, ctx, url: Option(str, "The youtube URL of the song you want to play")):
        if ctx.author.voice is None:
            await ctx.respond("You're not in a VC!", ephemeral=True)
        voiceChannel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voiceChannel.connect()
        else:
            await ctx.voice_client.move_to(voiceChannel)
        musicMsg = await ctx.respond("Loading your song...")
        vc = ctx.voice_client
        player = await YTDLSource.from_url(url, loop=False, stream=True)
        Vidtitle = player.title
        vidUrl = player.url
        channelName = player.uploader
        channelUrl = player.channel_url
        if len(self.queue) == 0:
            musicEmbed = Embed(title=f"Now Playing: {Vidtitle}", description=f"Video: [{Vidtitle}]({vidUrl})\nChannel: [{channelName}]({channelUrl})", color=0xFF0000)
            musicEmbed.set_thumbnail(url=player.thumbnail)
            self.start_playing(ctx, player)
            await ctx.respond(embed=musicEmbed)
        else:
            musicEmbed = Embed(title=f"Added to queue: {Vidtitle}", description=f"Video: [{Vidtitle}]({vidUrl})\nChannel: [{channelName}]({channelUrl})", color=0xFF0000)
            musicEmbed.set_thumbnail(url=player.thumbnail)
            self.queue.insert(len(self.queue), player)
            await ctx.respond(embed=musicEmbed)

    @slash_command(guild_ids=guild_ids, name="pause", description="Pauses the song")
    async def _pause(self, ctx):
        if ctx.voice_client is None:
            await ctx.respond("You're not in a VC!", ephemeral=True)
        else:
                if ctx.voice_client.is_playing():
                    ctx.voice_client.pause()
                    await ctx.respond("Paused!", ephemeral=True)
                else:
                    await ctx.respond("Already paused!", ephemeral=True)

    @slash_command(guild_ids=guild_ids, name="resume", description="Resumes the song")
    async def _resume(self, ctx):
        if ctx.voice_client is None:
            await ctx.respond("You're not in a VC!", ephemeral=True)
        else:
            if ctx.voice_client.is_paused():
                ctx.voice_client.resume()
                await ctx.respond("Resumed!", ephemeral=True)
            else:
                await ctx.respond("Already playing!", ephemeral=True)

    @slash_command(guild_ids=guild_ids, name="queue", description="Shows the song queue")
    async def _queue(self, ctx):
        print(self.queue)
        desc_string = ""
        num = 0
        for player in self.queue:
            num += 1
            if num == len(self.queue):
                desc_string += f"**{num}** | [{player.title}]({player.url})"
            else:
                desc_string += f"**{num}**| [{player.title}]({player.url})\n"
        embed = discord.Embed(title="Here's the queue!", description=desc_string, color=0xFF0000)
        await ctx.respond(embed=embed)

    @slash_command(guild_ids=guild_ids, name="skip", description="Skips the current song")
    async def _skip(self, ctx):
        vc = ctx.voice_client
        currentPlaying = self.queue[0]
        self.queue.pop(0)
        vc.stop()
        newPlayer = self.queue[1]
        self.start_playing(vc, newPlayer)




def setup(client):
    client.add_cog(Music(client))
