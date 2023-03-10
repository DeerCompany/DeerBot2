import discord
from discord.ext import commands
import pyttsx3


class VOICE():
    def __init__(self):
        pass

    async def voice(self, ctx, bot, command = None):
        global server, server_id, name_channel
        author = ctx.author

        params = command.split('!voice')
        engine = pyttsx3.init()
        engine.save_to_file(params, 'sound/voice.mp3')
        engine.runAndWait()

        if len(params) == 1:
            server = ctx.guild
            name_channel = author.voice.channel.name
            voice_channel = discord.utils.get(server.voice_channels, name = name_channel)
        else:
            await ctx.channel.send(f'{author.mention}, команда не коректна!')
            return

        voice = discord.utils.get(bot.voice_clients, guild = server)

        if voice is None:
            await voice_channel.connect()
            voice = discord.utils.get(bot.voice_clients, guild = server)

        voice.play(discord.FFmpegPCMAudio(executable='ffmpeg/bin/ffmpeg.exe',  source='sound/voice.mp3'))