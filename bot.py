import discord, os, urllib.request, re, asyncio
from discord.ext import commands
from config import config
from pytube import YouTube
from urllib.parse import quote 
from classes.ssp import SSP
from classes.voice import VOICE
from classes.clear import CLEAR

bot = commands.Bot(command_prefix=config['prefix'], intents=discord.Intents.all())


# Music
@bot.event
async def on_ready():
    print("Bot online!")

server, server_id, name_channel = None, None, None

domains = ['https://www.youtube.com/', 'http://www.youtube.com/', 'https://youtu.be/', 'http://youtu.be/']
async def check_domains(link):
    for x in domains:
        if link.startswith(x):
            return True
    return False


@bot.command()
async def play(ctx, *, command = None):
    name = ctx.channel.name
    #print(name)
    if name == "music" or "тест":
        global server, server_id, name_channel
        author = ctx.author
        if command == None:
            server = ctx.guild
            name_channel = author.voice.channel.name
            voice_channel = discord.utils.get(server.voice_channels, name = name_channel)

        params = command.split('!play')
        search_keyword = command
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + quote(search_keyword))
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        video_url = "https://www.youtube.com/watch?v=" + video_ids[0]
        
        if len(params) == 1:
            source = video_url
            server = ctx.guild
            name_channel = author.voice.channel.name
            voice_channel = discord.utils.get(server.voice_channels, name = name_channel)
        elif len(params) == 3:
            server_id = params[0]
            voice_id = params[1]
            source = video_url
            try:
                server_id = int(server_id)
                voice_id = int(voice_id)
            except:
                await ctx.channel.send(f'{author.mention}, id сервера або голосового канаду недійсне!')
                return
            server = bot.get_guild(server_id)
            voice_channel = discord.utils.get(server.voice_channels, id=voice_id)
        else:
            await ctx.channel.send(f'{author.mention}, команда не коректна!')
            return
        
        voice = discord.utils.get(bot.voice_clients, guild = server)

        if voice is None:
            await voice_channel.connect()
            voice = discord.utils.get(bot.voice_clients, guild = server)

        if source == None:
            pass
        elif source.startswith('http'):
            if not await check_domains(source):
                await ctx.channel.send(f'{author.mention}, посилання некоректне!')
                return
            song_there = os.path.isfile('song.mp3')
            try:
                if song_there:
                        os.remove('song.mp3')
            except PermissionError:
                await ctx.channel.send('Недостаньо прав для видалення!')

            url = str([source])
            yt = YouTube(url)
            video = yt.streams.filter(only_audio=True).first()
            downloaded_file = video.download()
            os.rename(downloaded_file, 'song.mp3')
            print("Done") 

            voice.play(discord.FFmpegPCMAudio(executable='ffmpeg/bin/ffmpeg.exe', source='song.mp3'))
        else:
            voice.play(discord.FFmpegPCMAudio(executable='ffmpeg/bin/ffmpeg.exe',  source=f'{source}'))
    else:
       print(f"Команда не може виконатися у каналі {name}!")

@bot.command()
async def leave(ctx):
    global server, name_channel
    voice = discord.utils.get(bot.voice_clients, guild=server)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.channel.send(f'{ctx.autor.mention}, бот вийшов з каналу!')

@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = server)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.channel.send('Музика на паузі!')

@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = server)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.channel.send('Музика вже грає!')


@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = server)
    voice.stop()



#Filter
words = ['лох', 'криса', 'бан']
answer = ['га']

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    role = discord.utils.get(message.guild.roles, name='mute')
    msg = message.content.lower()

    if msg in words:
        await message.delete()
        await message.channel.send(f'{message.author}, мут. Причина мат!')
        await message.author.add_roles(role)
        await asyncio.sleep(60)
        await message.author.remove_roles(role)

    if msg in answer:
        await message.channel.send(f'{message.author.mention} Ногаааааааааааааа!')


#Clear chat
@bot.command()
#@commands.has_any_role('BomBitOs', 'King')
async def clear_all(ctx):
    await CLEAR().clear_all(ctx)


@bot.command()
#@commands.has_any_role('BomBitOs', 'King')
async def clear(ctx, command = None):
    await CLEAR().clear(ctx, command)



#Text to Voice message
@bot.command()
async def voice(ctx, *, command = None):
    await VOICE().main(ctx, bot, command)

#Game
@bot.command()
async def ssp(ctx):
    await SSP().main(ctx)

bot.run(config['token'])
