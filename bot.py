import discord, time
from discord.ext import commands
from config import config
from classes.music import MUSIC
from classes.filters import FILTERS
from classes.ssp import SSP
from classes.voice import VOICE
from classes.clear import CLEAR

bot = commands.Bot(command_prefix=config['prefix'], intents=discord.Intents.all())

f = open('logs.txt', 'a+', encoding='utf-8')
time1 = time.localtime()
time = time.strftime("%m/%d/%Y, %H:%M:%S", time1)

@bot.event
async def on_message(message):
   
    f.write(f'{time}   {message.author} в {message.channel}: {message.content}\n') 


    @bot.event
    async def on_ready():
        print("Bot online!")

    

    #Play
    @bot.command()
    async def play(ctx, *, command = None):
        print(ctx, command)
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

f.close

bot.run(config['token'])
