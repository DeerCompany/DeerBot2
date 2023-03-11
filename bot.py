import discord, sys, time, asyncio
from discord.ext import commands
sys.path.insert(0, 'C:/Users/taras/OneDrive/Документи/python/deerhub')
from config import config
from classes.music import MUSIC
from classes.filters import FILTERS
from classes.ssp import SSP
from classes.voice import VOICE
from classes.clear import CLEAR
from classes.logs import LOGS
from classes.send_mail import MAIL

bot = commands.Bot(command_prefix=config['prefix'], intents=discord.Intents.all())

async def send_logs():
    x = "00:00", "10:00", "20:00"
    time1 = LOGS().tim()
    if time1 in x:
        MAIL().send_email()
        LOGS().on_message("Логи скинуто")
        time.sleep(61)
    else:
        await asyncio.sleep(30)
        await send_logs()

@bot.event
async def on_ready():
    await LOGS().on_message("Bot online!")
    print("Bot online!")
    await send_logs()


@bot.event
async def on_message(message):
    #Filter
    await FILTERS().filters(message, bot)
    #Logs
    await LOGS().on_message(message)
    if message.content == ("*send logs"):
        await send_logs()


@bot.event
async def on_voice_state_update(member, before, after):
    await LOGS().voice_logs(member, before, after)

#Play
@bot.command()
async def play(ctx, *, command = None):
    await MUSIC().play(ctx, command)

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
    await MUSIC().pause(ctx, bot) #покишо так


@bot.command()
async def repeat(ctx):
    await MUSIC().repeat(ctx)

@bot.command()
async def next(ctx):
    await MUSIC().next(ctx, bot)
@bot.command()
async def back(ctx):
    await MUSIC().back(ctx, bot)

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
    await VOICE().voice(ctx, bot, command)

#Game
@bot.command()
async def ssp(ctx):
    await SSP().ssp(ctx)

bot.run(config['token'])
