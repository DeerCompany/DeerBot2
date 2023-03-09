from time import time
import time

class LOGS():

    def __init__(self):
        time1 = time.strftime("%d.%m.%Y, %H:%M:%S", time.localtime())
        data = ""
        for datas in range(10):  data = data + time1[datas]
        f = open(f"Logs {data}", 'a+', encoding='utf-8')
        self.time = time1
        self.f = f
        f.close

    async def on_message(self, message):
        try:
            self.f.write(f'{self.time}  Сервер: {message.guild} - {message.author} написав в {message.channel}: {message.content}\n')
        except:
            self.f.write(f"{self.time}  {message}\n")


    async def voice_logs(self, member, before, after):
        if after.channel and after.channel!=before.channel:
            self.f.write(f"{self.time}   Сервер: {member.guild} - {member} зайшов в голосовий канал: {after.channel.name}\n")
        if before.channel and after.channel!=before.channel:
            self.f.write(f"{self.time}   Сервер: {member.guild} - {member} вийшов з голосового каналу: {before.channel.name}\n")

        if after.self_mute and after.self_mute!=before.self_mute:
            self.f.write(f"{self.time}   Сервер: {member.guild} - {member} замутився в голосовому каналі: {after.channel.name}\n")
        if before.self_mute and after.self_mute!=before.self_mute:
            self.f.write(f"{self.time}   Сервер: {member.guild} - {member} розмутився в голосовому каналі: {before.channel.name}\n")

        if after.mute and after.mute!=before.mute:
            self.f.write(f"{self.time}   Сервер: {member.guild} замутив {member} в голосовому каналі: {after.channel.name}\n")
        if before.mute and after.mute!=before.mute:
            self.f.write(f"{self.time}   Сервер: {member.guild} розмутив {member} в голосовому каналі: {after.channel.name}\n")