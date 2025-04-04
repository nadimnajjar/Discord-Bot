import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import random
from apikeys import *
import requests
import json
import asyncio
import yt_dlp

intents = discord.Intents.all()  
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('On :)')

@client.command()
async def hi(ctx):
    await ctx.send('Hello ! :)')



@client.command()
async def joke(ctx):
    

   url = "https://jokes-always.p.rapidapi.com/family"

   headers = {
        "x-rapidapi-key": MYAPI,
        "x-rapidapi-host": "jokes-always.p.rapidapi.com"
    }

   response = requests.get(url, headers=headers)
   channel=client.get_channel(1311509813477376041)
   await channel.send(json.loads(response.text)['data'])

@client.command(pass_context= True)
async def exit(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("BYE!")
    else:
        await ctx.send("You're not in the voice chat")
video_queue = []
is_playing = False
@client.command
async def table(ctx,width:int,*args):
    if len(args) % 2 != 0:
        await ctx.send("Erreur : Vous devez fournir un nombre pair d'arguments (clé-valeur).")
        return
    pairs = [(args[i], args[i + 1]) for i in range(0, len(args), 2)]
    
    table_content = ""
    for i, (key, value) in enumerate(pairs):
        table_content += f"`{key}`: {value}\n"
        if (i + 1) % width == 0:
            table_content += "\n"  

    embed = discord.Embed(
        title="Table générée",
        description=table_content,
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)
@client.command()
async def play(ctx, url):
    global is_playing
    if ctx.voice_client is None:
        await ctx.send(f"Please enter the voice chat in order for me to join")
        return
    video_queue.append(url)
    if not is_playing:
        await play_next(ctx)
    else:
        await ctx.send(f"The song is now in the queue. Queue: {len(video_queue)}")
async def play_next(ctx):
    global is_playing

    if len(video_queue) == 0:
        await ctx.send("Done with the songs :)")
        is_playing = False
        return

    is_playing = True
    url = video_queue.pop(0)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['url']
            title = info.get('title', 'Inconnu')
            audio_source=FFmpegPCMAudio(url2, options="-vn")
            ctx.voice_client.play(audio_source, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), client.loop))

            await ctx.send(f"🎶 Now playing: **{title}**")
    except Exception:
        pass

@client.event
async def on_voice_state_update(member, before, after):
    if client.user == member and after.channel is None:
        if before.channel is not None:
            vc = before.channel.guild.voice_client
            if vc:
                await vc.disconnect()
@client.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"I'm in {channel}")
    else:
        await ctx.send("Please enter the voice chat")

client.run(BOTTOKEN)