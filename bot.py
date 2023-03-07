import discord, os, urllib.request, re, asyncio
from discord.ext import commands
from config import config
from pytube import YouTube
from urllib.parse import quote 
from classes.music import MUSIC
from classes.filters import FILTERS
from classes.ssp import SSP
from classes.voice import VOICE
from classes.clear import CLEAR

bot = commands.Bot(command_prefix=config['prefix'], intents=discord.Intents.all())

# Music
@bot.event
async def on_ready():
    print("Bot online!")


#Play
@bot.command()
async def play(ctx, command = None):
    await MUSIC().play(ctx, command, bot)

@bot.command()
async def leave(ctx, command = None):
    await MUSIC().leave(ctx, bot)

@bot.command()
async def pause(ctx, command = None):
    await MUSIC().pause(ctx, bot)

@bot.command()
async def resume(ctx, command = None):
    await MUSIC().resume(ctx, bot)

@bot.command()
async def stop(ctx, command = None):
    await MUSIC().stop(bot)


#Filter
@bot.event
async def on_message(message):
   await FILTERS().filters(message, bot)


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
