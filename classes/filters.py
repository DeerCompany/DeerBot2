import discord, os, urllib.request, re, asyncio
from discord.ext import commands

class FILTERS():
    def __init__(self):
        pass

    async def filters(self, message, bot):
        words = ['лох', 'криса', 'бан']
        answer = ['га'] 
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