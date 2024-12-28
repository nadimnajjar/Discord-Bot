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
    await ctx.send('LAK HIIIIIIIIII')

@client.command()
async def seb(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send(f"@?")
    else:
        await ctx.send(f"Ayre b {member.mention} ")


@client.command()
async def cock_size(ctx,member: discord.Member = None):
    if member is None:
        await ctx.send(f"badna n2is er min hbb")
    else:
        await ctx.send('8'+'='*random.randint(1,20)+'D')
@client.command()
async def gay_rate(ctx,member: discord.Member = None):
    if member is None:
        print(f"@?")
    else:
        await ctx.send(f'{discord.Member}\'s gayrate is {random.randint(1,100)}%')
@client.command()
async def indus(ctx):
    await ctx.send(f"LES INDUS SONT DES IDIOTS IYAA IYAA OHHHHH")

@client.command()
async def seb_nabih(ctx):
    await ctx.send(f"ayre b nabih")

@client.command()
async def seb_hadi(ctx):
    await ctx.send("Ayre b Hadi")

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
async def dhar(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Yalla salam")
    else:
        await ctx.send("Manne jowa la etla3 ya hmar")
video_queue = []
is_playing = False
@client.command
async def table(ctx,width:int,*args):
    if len(args) % 2 != 0:
        await ctx.send("Erreur : Vous devez fournir un nombre pair d'arguments (clé-valeur).")
        return

    # Regrouper les arguments en paires clé-valeur
    pairs = [(args[i], args[i + 1]) for i in range(0, len(args), 2)]
    
    # Créer une table formatée
    table_content = ""
    for i, (key, value) in enumerate(pairs):
        table_content += f"`{key}`: {value}\n"
        if (i + 1) % width == 0:
            table_content += "\n"  # Ajouter une ligne vide pour séparer les rangées

    # Créer un embed pour afficher la table
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
        await ctx.send(f"Ntek foot aal voice chat abel ma t7ot el command ya er")
        return
    video_queue.append(url)
    if not is_playing:
        await play_next(ctx)
    else:
        await ctx.send(f"Haye hatayneya bel queue fa rawi2 tizak. Queue: {len(video_queue)}")
async def play_next(ctx):
    global is_playing

    if len(video_queue) == 0:
        await ctx.send("5allasna aghene")
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

            await ctx.send(f"🎶 SHA8EL YA KBIR **{title}**")
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
async def sharrif(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"fetet 3ala {channel}")
    else:
        await ctx.send("badak tkoon jowa la foot ya hmar")

client.run(BOTTOKEN)