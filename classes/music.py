import discord, os, urllib.request, re, asyncio
from discord.ext import commands
from pytube import YouTube
from urllib.parse import quote 


class MUSIC():
    def __init__(self):
        pass

    server, server_id, name_channel = None, None, None



    async def play(self, ctx, command, bot):
        domains = ['https://www.youtube.com/', 'http://www.youtube.com/', 'https://youtu.be/', 'http://youtu.be/']
        async def check_domains(link):
            for x in domains:
                if link.startswith(x):
                    return True
            return False
        
        name = ctx.channel.name
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



    async def leave(self, ctx, bot):
        global server, name_channel
        voice = discord.utils.get(bot.voice_clients, guild=server)
        if voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.channel.send(f'{ctx.autor.mention}, бот вийшов з каналу!')


    async def pause(self, ctx, bot):
        voice = discord.utils.get(bot.voice_clients, guild = server)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.channel.send('Музика на паузі!')


    async def resume(self, ctx, bot):
        voice = discord.utils.get(bot.voice_clients, guild = server)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.channel.send('Музика вже грає!')


    async def stop(self, bot):
        voice = discord.utils.get(bot.voice_clients, guild = server)
        voice.stop()