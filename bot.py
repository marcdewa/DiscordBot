# bot.py
import os
import shutil
import asyncio
import discord
import export as export
# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
import youtube_dl
from discord.utils import get
from discord.ext import commands

# spotipy.util.prompt_for_user_token(username, scope, client_id='your-spotify-client-id', client_secret='your-spotify-client-secret', redirect_uri='your-app-redirect-url')
# client = discord.Client()
# GUILD = '540197125200412702'
client = discord.Client()
botCommand = commands.Bot(command_prefix='.')

players = {}


@botCommand.event
async def on_ready():
    print(
        f'{client.user} is connected to the following guild:\n'
    )

voice = None


@botCommand.command(pass_context=True)
async def plays(ctx, url):
    server = ctx.message.guild
    global voice
    channel = ctx.message.author.voice.channel
    # voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await ctx.send(f"Joined {channel}")
    # if voice is None:
    #     voice = await channel.connect()
    # song_there = os.path.isfile("song.mp3")

    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queue\n")
                #asyncio.queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song done , playing next queue\n")
                print(f"song still in queue: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: print('done', e))
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07
            else:
                #asyncio.queues.clear()
                return
        else:
            #asyncio.queues.clear()
            print("No song founds")

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            #asyncio.queues.clear()
            print("remove old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR : Music Playing")
        return

    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Removed old Queue folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No old queue folder")

    await ctx.send("Getting everything ready now")

    # voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"renamed file : {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: print('done', e))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname= name.rsplit("-",2)
    await ctx.send(f"Playing {nname[0]}")
    print("Playing\n")

    # global voice
    # if voice is None:
    #     voice = await channel.connect()

    # song_there = os.path.isfile("song.mp3")
    # try:
    #     if song_there:
    #         os.remove("song.mp3")
    # except PermissionError:
    #     print("Trying to delete song file, but it's being played")
    #     return


@botCommand.command(pass_context=True)
async def ping(ctx):
    await ctx.send('test')


@botCommand.command(pass_context=True)
async def join(ctx):
    global vc
    channel = ctx.message.author.voice.channel
    vc = channel.connect()
    await channel.connect()


# @botCommand.command(pass_context=True)
# async def spotify(ctx):
#     birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
#     spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
#
#     results = spotify.artist_albums(birdy_uri, album_type='album')
#     albums = results['items']
#     while results['next']:
#         results = spotify.next(results)
#         albums.extend(results['items'])
#
#     for album in albums:
#         print(album['name'])


@botCommand.event
async def on_message(message):
    if message.author == client.user:
        return

    msg1 = '<@333863300892721152> davis kok pepe ya'

    if message.content == 'command list':
        await message.channel.send('- davis mah\n- davis\n- .plays + youtubeURL')

    if message.content == 'davis mah':
        for x in range(3):
            await message.channel.send('davis mah paling jago')
    if message.content == 'davis':
        response = msg1
        for x in range(3):
            await message.channel.send(response)
    if message.content == 'bel sama jessica':
        response = 'jessica lah , https://imgur.com/TrtyIVa'
        await message.channel.send(response)
    if message.content == 'ig jessica':
        response = 'https://www.instagram.com/h.yojeong/'
        await message.channel.send(response)
    await botCommand.process_commands(message)


# @botCommand.command(pass_context=True)
# async def play(ctx, url):
#     await join(ctx)
#     server = ctx.message.server
#     voice_client = client.voice_client_in(server)
#     player = await voice_client.create_ytdl_player(url)
#     players[server.id] = player
#     player.start()


# client.run('NzI0NzExNzQwNDQwNTc2MDgy.XvEesA.SC0bf4GMJdL3gAVSZIUuYcgjHa8')
botCommand.run('NzI0NzExNzQwNDQwNTc2MDgy.XvEesA.SC0bf4GMJdL3gAVSZIUuYcgjHa8')
