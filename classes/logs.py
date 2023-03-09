import time

class LOGS():
    def __init__(self):
        pass

    async def message_logs(self, message):
       get_time = time.strftime("%d.%m.%Y, %H:%M:%S", time.localtime()) 

       f = open("logs.txt", "a+", encoding="utf-8")
       f.write(f'{get_time}  Сервер: {message.guild} - {message.author} написав в {message.channel}: {message.content}\n')
       f.close

    async def voice_logs(self, member, before, after):
        if after.channel and after.channel!=before.channel:
            print(f"Користувач {member} зайшов в голосовий канал: {after.channel.name}")
        if before.channel and after.channel!=before.channel:
            print(f"Користувач {member} вийшов з голосового каналу: {after.channel.name}")
