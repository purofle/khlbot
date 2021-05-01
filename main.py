import asyncio
from application import KaiHeiLaApplication
from application.event.kaiheila import TextMessageEvent
from graia.broadcast import Broadcast
from config import token
from application.group import Member

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)

app = KaiHeiLaApplication(token=token, broadcast=bcc, debug=True)


@bcc.receiver(TextMessageEvent)
async def tme(app: KaiHeiLaApplication, event: TextMessageEvent, text: str):
    if text.startswith("复读"):
        await app.sendGroupMessage(event.target_id, text[2:])


app.launch()
