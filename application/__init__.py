import asyncio
import json
import logging
from yarl import URL
from .utils import raise_for_return_code
from aiohttp import ClientSession
from aiohttp.http_websocket import WSMsgType

class KaiHeiLaApplication:
    def __init__(
            self,
            token: str,
            loop: asyncio.AbstractEventLoop = None
            ) -> None:
        self.baseURL = "https://www.kaiheila.cn/api"
        self.loop = loop or asyncio.get_event_loop()
        self.token = token
        self.session = ClientSession(
                loop=loop,
                headers={
                    "Authorization": "Bot {}".format(self.token)
                    }
                )
        self.gateway: str = ""
        self.logger: log

    def url_gen(self, path: str) -> str:
        return str(URL(self.baseURL) / "v3" / path)

    async def getGateway(self) -> str:
        async with self.session.get(
                self.url_gen("gateway/index")+"/?compress=0") as resp:
            resp.raise_for_status()
            data = await resp.json()
            raise_for_return_code(data)
            gateway = data["data"]["url"]
            self.gateway = gateway
            return gateway

    async def ws_hello(self):
        async with self.session.ws_connect(
                self.gateway,
                timeout=6.0,
                autoping=False
                ) as ws:
            try:
                while True:
                    message = await ws.receive()
                    print(message.data)
                    if message.type == WSMsgType.TEXT:
                        data = json.loads(message.data)
            except ValueError as e:
                print(e)


    async def stop(self):
        await self.session.close()
    
    async def main(self):
        await self.getGateway()
        await self.ws_hello()

    def launch(self):
        try:
            print(self.loop.run_until_complete(self.main()))
        finally:
            self.loop.run_until_complete(self.stop())
