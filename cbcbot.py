import discord
import asyncio
import datetime
import json

week_day_names_rus = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']

def make_msg(cbev):
    return week_day_names_rus[cbev['weekday']-1]+' '+str(cbev['hour']).zfill(2)+':'+str(cbev['min']).zfill(2)+' '+cbev['name']

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print('[',self.user.id,'] ',self.user.name,sep='')
        for cbev in cbevents:
            print(make_msg(cbev))

    async def my_background_task(self):
        await self.wait_until_ready()

        while not self.is_closed():
            now = datetime.datetime.now()
            for cbev in cbevents:
                if now.hour == cbev['hour'] and now.minute == cbev['min'] and now.isoweekday() == cbev['weekday']:
                    msg = make_msg(cbev)
                    channel = self.get_channel(settings['channelid'])
                    await channel.send(msg)
                    print(msg)

            await asyncio.sleep(60)

with open("./calendar.json", "r",encoding="utf-8") as read_file:
    cbevents = json.load(read_file)

with open("./settings.json", "r",encoding="utf-8") as read_file:
    settings = json.load(read_file)

client = MyClient()
client.run(settings['token'])
