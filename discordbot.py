import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from youtube_dl import YoutubeDL
from discord import VoiceChannel
import urllib.request
import re

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('Musicbot ready')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='bangers'))

@client.command(aliases=["j"])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
        await ctx.send(':x: **already connected**')    
    else:
        voice = await channel.connect()
        await ctx.send(':thumbsup: **joined**')   

@client.command(aliases=["l"])
async def leave(ctx):
  voice = get(client.voice_clients, guild=ctx.guild)
  if voice and voice.is_connected():
    await ctx.voice_client.disconnect()
    await ctx.send(':thumbsup: **disconnected**')
  else:
    await ctx.send(':x: **I am not in any voicechat..**')

@client.command(aliases=["p"])
async def play(ctx, url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        
    voice = get(client.voice_clients, guild=ctx.guild)
    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.send(':notes: **Playing**')
    else:
        await ctx.send(":x: **The bot is already playing..**")
        return

@client.command(aliases=["se"])
async def search(ctx, *, text):
  keyword = text.replace(" ", "+")
  html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + keyword)
  video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
  final_url = ("https://www.youtube.com/watch?v=" + video_ids[0])
  
  voice = get(client.voice_clients, guild=ctx.guild)
  if not voice.is_playing():
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    with YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(final_url, download=False)
    URL = info['url']
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    voice.is_playing()
    await ctx.send(':notes: **Playing:**')
    await ctx.send(final_url)
  else:
      await ctx.send(":x: **The bot is already playing..**")
      return

@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        voice.resume()
        await ctx.send(':play_pause: **Resuming..**')


@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
        await ctx.send(':pause_button: **Pausing..**')


@client.command(aliases=["fs", "s", "skip"])
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()
        await ctx.send(':x: **Stopping..**')

client.run('INSERT YOUR TOKEN')