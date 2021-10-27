import os

import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
# load our local env so we don't have the token in public
from dotenv import load_dotenv
from youtube_dl import YoutubeDL

load_dotenv()
client = commands.Bot(command_prefix='!')  # prefix'!'

players = {}


@client.event  # check if bot is ready
async def on_ready():
    print('Bot online')


# command for bot to join the channel of the user, if the bot has already joined and is in a different channel,
# it will move to the channel the user is in
@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        await channel.connect()


# command to play sound from a youtube URL
@client.command()
async def play(ctx, url):
    ydl_options = {'format': 'bestaudio', 'noplaylist': 'true'}
    ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with YoutubeDL(ydl_options) as ydl:
            info = ydl.extract_info(url, download=False)
        url = info['url']
        voice.play(FFmpegPCMAudio(url, **ffmpeg_options))
        voice.is_playing()
        await ctx.send('Bot is playing')

# check if the bot is already playing
    else:
        await ctx.send("Bot is already playing")
        return


# command to resume voice if it is paused
@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        voice.resume()
        await ctx.send('Bot is resuming')


# command to pause voice if it is playing
@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
        await ctx.send('Bot has been paused')


# command to stop voice
@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()
        await ctx.send('Stopping...')


# command to clear channel messages
@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send("Messages have been cleared")


client.run(os.getenv('TOKEN'))
