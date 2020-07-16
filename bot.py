# bot.py
import os
import shutil
import discord
import youtube_dl
from discord.ext import commands
import urllib.parse
import urllib.request
import re

client = discord.Client()
botCommand = commands.Bot(command_prefix='.')

players = {}


@botCommand.event
async def on_ready():
    print(
        f'{client.user} is connected to the following guild:\n'
    )

@botCommand.command(pass_context=True, aliases=['y'])
async def youtube(ctx,*,search):
    query_string = urllib.parse.urlencode({
        'search_query': search
    })

    htm_content = urllib.request.urlopen(
        'http://www.youtube.com/results?' + query_string
    )
    print(r'/watch\?v=(.{11})')

    search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode('utf-8'))
    await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])

voice = None

q_num=0

@botCommand.command(pass_context=True, aliases=['p', 'play'])
async def plays(ctx,*,url):
    server = ctx.message.guild
    global voice
    channel = ctx.message.author.voice.channel
    if not str(url).startswith('http'):
        query_string = urllib.parse.urlencode({
            'search_query': url
        })

        htm_content = urllib.request.urlopen(
            'http://www.youtube.com/results?' + query_string
        )
        print(r'/watch\?v=(.{11})')

        search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode('utf-8'))
        url = 'http://www.youtube.com/watch?v=' + search_results[0]

    if voice:
        print("ok")
    else:

        voice = await channel.connect()
    await ctx.send(f"Joined {channel}")
    # if voice is None:
    #     voice = await channel.connect()
    # song_there = os.path.isfile("song.mp3")

    def check_queue():
        print('Test')
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queue\n")
                queues.clear()
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

                voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07
            else:
                queues.clear()
                return
        else:
            queues.clear()
            print("No song founds")


    def add_queue():
        print("Test")
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is False:
            os.mkdir("Queue")
        DIR = os.path.abspath(os.path.realpath("Queue"))
        q_num = len(os.listdir(DIR))
        q_num += 1
        add_queue = True
        while add_queue:
            if q_num in queues:
                q_num += 1
            else:
                add_queue = False
                queues[q_num] = q_num

        queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'outtmpl': queue_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])


        print("Song added to queue\n")

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("remove old song file")
    except PermissionError:
        add_queue()
        await ctx.send("Adding song to the queue")
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

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 1)
    await ctx.send(f"Playing {nname[0]}")
    print("Playing\n")


queues = {}

@botCommand.command(pass_context=True)
async def ping(ctx):
    await ctx.send('test')


@botCommand.command(pass_context=True)
async def join(ctx):
    global vc
    channel = ctx.message.author.voice.channel
    vc = channel.connect()
    await channel.connect()

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


# client.run('NzI0NzExNzQwNDQwNTc2MDgy.XvEesA.SC0bf4GMJdL3gAVSZIUuYcgjHa8')
botCommand.run('NzI0NzExNzQwNDQwNTc2MDgy.Xw9Asg.Gk0nvT0kg9dCIpVml9bHSXOtmnY')
