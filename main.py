import asyncio
from application import KaiHeiLaApplication
from application.event.kaiheila import GroupMessage
from graia.broadcast import Broadcast
from config import token
from application.group import Member

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)

app = KaiHeiLaApplication(token=token, broadcast=bcc)


@bcc.receiver(GroupMessage)
async def tme(kha: KaiHeiLaApplication, member: Member, message: str):
    print("收到消息：{}".format(message))
    print(member.id)


app.launch()
