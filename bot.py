import discord
from discord.ext import commands
from ..DeerHub.config import config
from classes.music import MUSIC
from classes.filters import FILTERS
from classes.ssp import SSP
from classes.voice import VOICE
from classes.clear import CLEAR
from classes.logs import LOGS

bot = commands.Bot(command_prefix=config['prefix'], intents=discord.Intents.all())

@bot.event
async def on_ready():
    await LOGS().on_message("Bot online!")
    print("Bot online!")


@bot.event
async def on_message(message):
    #Filter
    await FILTERS().filters(message, bot)
    
    #Logs
    await LOGS().on_message(message)

@bot.event
async def on_voice_state_update(member, before, after):
    await LOGS().voice_logs(member, before, after)

#Play
@bot.command()
async def play(ctx, *, command = None):
    await MUSIC().play(ctx, command, bot)

@bot.command()
async def leave(ctx):
    await MUSIC().leave(ctx, bot)

@bot.command()
async def pause(ctx):
    await MUSIC().pause(ctx, bot)

@bot.command()
async def resume(ctx):
    await MUSIC().resume(ctx, bot)

@bot.command()
async def stop(ctx):
    await MUSIC().stop(bot)

#Clear chat
@bot.command()
async def clear_all(ctx):
    await CLEAR().clear_all(ctx)

@bot.command()
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
