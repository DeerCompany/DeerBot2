import discord
from discord.ui import Button, View

# async def my_print(mess, message): # Завжди робочий варіант!!!
#     await message.channel.send(mess)


class SSP():
    def __init__(self):
        pass

    async def win(self, players, message):
        iterObj = iter(players); keys = list(iterObj)


        players1 = players.get(keys[0])
        players2 = players.get(keys[1])
        #players3 = players.get(keys[2])


        async def stone1():
            if players1 == players2:
                await message.channel.send("Нічия")
            elif players2 == "Paper":
                await message.channel.send(f"{keys[1]} виграв.")
            else:
                await message.channel.send(f"{keys[0]} виграв.")


        async def scissors1():
            if players1 == players2:
                await message.channel.send("Нічия")
            elif players2 == "Stone":
                await message.channel.send(f"{keys[1]} виграв.")
            else:
                await message.channel.send(f"{keys[0]} виграв.")


        async def paper1():
            if players1 == players2:
                await message.channel.send("Нічия")
            elif players2 == "Scissors":
                await message.channel.send(f"{keys[1]} виграв.")
            else:
                await message.channel.send(f"{keys[0]} виграв.")


        if players1 == "Stone":
            await stone1()
            players.clear() 
        elif players1 == "Scissors":
            await scissors1()
            players.clear() 
        else:
            await paper1()
            players.clear() 

    
    async def ssp(self, ctx):
        message=ctx
        
        n = 2  # Кількість гравців
        players = {}

        button1 = Button(label="Камінь", style=discord.ButtonStyle.green, emoji='🪨')
        button2 = Button(label="Ножиці", style=discord.ButtonStyle.green, emoji='✂️')
        button3 = Button(label="Папір", style=discord.ButtonStyle.green, emoji='📃')

        async def button_stone(interaction):
            await interaction.response.defer()
            players.update([(f"{interaction.user}", "Stone")])
            if len(players) == n:
                await SSP.win(self, players, message)
            else:
                pass

        async def button_scissors(interaction):
            await interaction.response.defer()
            players.update([(f"{interaction.user}", "Scissors")])
            if len(players) == n:
                await SSP.win(self, players, message)
            else:
                pass

        async def button_paper(interaction):
            await interaction.response.defer()
            players.update([(f"{interaction.user}", "Paper")])
            if len(players) == n:
                await SSP.win(self, players, message)
            else:
                pass

        button1.callback = button_stone
        button2.callback = button_scissors
        button3.callback = button_paper

        view = View()
        view.add_item(button1)
        view.add_item(button2) 
        view.add_item(button3)
        await message.send(view = view)
