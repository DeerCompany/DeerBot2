import discord, os, urllib.request, re, time, asyncio
from discord.ext import commands
from pytube import YouTube
from urllib.parse import quote
from classes.logs import LOGS


class MUSIC():
    def __init__(self):
        pass

    server, server_id, name_channel =  None, None, None
    global music_list
    music_list = ["https://www.youtube.com/watch?v=oMfMUfgjiLg&ab_channel=GunsN%27Roses-Topic"]
    async def play(self, ctx, command):
        domains = ['https://www.youtube.com/', 'http://www.youtube.com/', 'https://youtu.be/', 'http://youtu.be/']
        async def check_domains(link):
            for x in domains:
                if link.startswith(x):
                    return True
            return False
        
        name = ctx.channel.name
        if name == "music" or "тест":
            global server, server_id, name_channel, source, vc
            author = ctx.author
            if command == None:
                server = ctx.guild
                name_channel = author.voice.channel.name
            
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + quote(command))
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            source = "https://www.youtube.com/watch?v=" + video_ids[0]
            if len(command.split('!play')) == 1:
                server = ctx.guild
                name_channel = author.voice.channel.name
            else:
                await ctx.channel.send(f'{author.mention}, команда не коректна!')
                return
            

            if source.startswith('http'):
                if not await check_domains(source):
                    await ctx.channel.send(f'{author.mention}, посилання некоректне!')
                    return
                
                try:
                    voice_channel = discord.utils.get(server.voice_channels, name = name_channel)
                    vc = await voice_channel.connect()
                except:
                    if vc.is_playing():
                        await ctx.channel.send('Музика вже грає!')
                        music_list.append(source)
                        print(music_list)
                        return
                    else:
                        if command == command:
                            pass
                        else:
                            await ctx.channel.send('Вже підключений!')


                yt = YouTube(str([source]))
                video = yt.streams.filter(only_audio=True).first()
                downloaded_file = video.download()
                os.remove('sound/music.mp3')
                os.rename(downloaded_file, 'sound/music.mp3')

                await LOGS().on_message(message=(f"Скачано  {command} - {source}"))

                

                vc.play(discord.FFmpegPCMAudio(executable='ffmpeg/bin/ffmpeg.exe', source='sound/music.mp3'))
            else:
                vc.play(discord.FFmpegPCMAudio(executable='ffmpeg/bin/ffmpeg.exe',  source=f'{source}'))


            # while vc.is_playing():
            #     await asyncio.sleep(2)
            # if not vc.is_paused():
            #     if len(music_list) > 0:
            #         line = music_list[0]
            #         music_list = music_list[1:]
            #         await MUSIC().play(ctx, line)

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

    async def repeat(self, ctx):
        await MUSIC().play(ctx, command=source)