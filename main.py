import asyncio
import logging
import os

import discord
import yt_dlp
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
intents = discord.Intents.all()

client = discord.Client(command_prefix="!", intents=intents)

songs = {}


def get_song_info(url):
    ydl_opts = {
        'format': 'bestaudio/best',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)

    return info_dict


# create a function to play a song
async def play_song(ctx, info_dict):
    voice_channel = ctx.author.voice.channel
    if client.voice_clients:
        await client.voice_clients[0].stop()

    voice_client = await voice_channel.connect()
    song_url = info_dict.get('url', None)
    if song_url is not None:
        voice_client.play(discord.FFmpegPCMAudio(song_url, options='-vn'),
                          after=lambda e: print('Player error: %s' % e) if e else None)
    else:
        print(f'Didn`t find a song for {song_url}')
    voice_client.source = discord.PCMVolumeTransformer(voice_client.source, 1)


async def handle_command(ctx, cmd):
    global songs
    if cmd.startswith('!play'):
        url = cmd.split()[1]
        info_dict = get_song_info(url)

        await play_song(ctx, info_dict)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!'):
        await handle_command(message, message.content)


# run the client
client.run(TOKEN)
