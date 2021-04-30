import asyncio
from application import KaiHeiLaApplication
from application.event.kaiheila import TextMessageEvent
from graia.broadcast import Broadcast
from config import token

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)

app = KaiHeiLaApplication(token=token, broadcast=bcc, debug=True)

@bcc.receiver(TextMessageEvent)
async def tme(event: TextMessageEvent):
    print(event.text)

app.launch()
