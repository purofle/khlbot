import asyncio
from application import KaiHeiLaApplication
from graia.broadcast import Broadcast
from config import token

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)

KaiHeiLaApplication(token=token, broadcast=bcc, debug=True).launch()
