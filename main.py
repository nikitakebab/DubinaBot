import logging

import discord
import yt_dlp

# import os
# os.environ['FFMPEG_PATH'] = 'C:/ProgramData/chocolatey/bin/ffmpeg.exe'

intents = discord.Intents.all()
# create a Discord client
client = discord.Client(command_prefix="!", intents=intents)
# client = commands.AutoShardedBot(command_prefix='!', intents=intents)

# create a dictionary to store the songs
songs = {}


# create a function to extract the audio from a YouTube video and save it as an MP3 file
def download_song(url):
    # ydl_opts = {
    #     'format': 'bestaudio/best',
    #     # 'outtmpl': 'output.mp3',
    #     'postprocessors': [
    #         {
    #             'key': 'FFmpegExtractAudio',
    #             'preferredcodec': 'mp3',
    #             'preferredquality': '192'
    #         }
    #     ],
    #     # 'audioformat': 'mp3',  # convert to mp3
    #     # 'ffmpeg_location': 'C:/ProgramData/chocolatey/bin/ffmpeg.exe',
    #     'nopostoverwrites': False
    #     # 'progress_hooks': [print],  # optional hook to print progress
    #     # 'ffmpeg_path': 'C:/ProgramData/chocolatey/bin/ffmpeg.exe'  # path to ffmpeg executable
    # }

    ydl_opts = {
        'format': 'bestaudio/best',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)

    return info_dict


# create a function to play a song
async def play_song(ctx, info_dict):
    # get the voice channel that the user is in
    voice_channel = ctx.author.voice.channel
    # check if the bot is already playing a song
    if client.voice_clients:
        # stop playing the current song
        await client.voice_clients[0].stop()
    # create a new voice client
    voice_client = await voice_channel.connect()
    # get the path to the MP3 file
    # path = songs[song]
    # create a new subprocess to play the song
    # subprocess.Popen(['ffmpeg', '-i', path, '-f', 'mp3', '-'], stdout=subprocess.PIPE)
    # play the song
    voice_client.play(discord.FFmpegPCMAudio(info_dict.get('url', None), options='-vn'), after=lambda e: print('Player error: %s' % e) if e else None)
    voice_client.source = discord.PCMVolumeTransformer(voice_client.source, 1)
    # wait for the song to finish playing
    # while voice_client.is_playing():
    # await asyncio.sleep(1)
    # disconnect from the voice channel
    # await voice_client.disconnect()


# create a function to handle commands
async def handle_command(ctx, cmd):
    global songs
    # check if the command is to play a song
    if cmd.startswith('!play'):
        # get the URL of the song
        url = cmd.split()[1]
        # download the song and save it to the songs dictionary
        info_dict = download_song(url)
        # songs[title] = f'{title}.mp3'

        # play the song
        await play_song(ctx, info_dict)


# create an event listener for when a message is sent in a server
@client.event
async def on_message(message):
    # ignore messages sent by the bot itself
    if message.author == client.user:
        return
    # check if the message starts with the command prefix
    if message.content.startswith('!'):
        # handle the command
        await handle_command(message, message.content)


# run the client
client.run("MTEwMDc4OTU2MTU4OTc2NDE3OA.GafM25.Paw3mlKPydmeYWSMDeHk6NrUfpL_TgyvttZ_Ss", log_level=logging.DEBUG)
