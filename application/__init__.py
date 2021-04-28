import asyncio
import json
from typing import Optional
from yarl import URL
from .utils import raise_for_return_code
from . import logger
from aiohttp import ClientSession
from aiohttp.http_websocket import WSMsgType
from aiohttp.client_ws import ClientWebSocketResponse
from graia.broadcast import Broadcast


class KaiHeiLaApplication:


    def __init__(
        self,
        token: str,
        broadcast: Broadcast,
        debug: bool = False
    ) -> None:
        self.broadcast = broadcast
        self.baseURL = "https://www.kaiheila.cn/api"
        self.token = token
        self.session = ClientSession(
            loop=broadcast.loop, headers={"Authorization": "Bot {}".format(self.token)}
        )
        self.gateway: str = ""
        self.logger = logger.LoggingLogger(**{"debug": True} if debug else {})
        self.buffer = {"sn": 0}

    def url_gen(self, path: str) -> str:
        return str(URL(self.baseURL) / "v3" / path)

    async def getGateway(self) -> str:
        async with self.session.get(
            self.url_gen("gateway/index") + "/?compress=0"
        ) as resp:
            resp.raise_for_status()
            data = await resp.json()
            raise_for_return_code(data)
            gateway = data["data"]["url"]
            self.gateway = gateway
            return gateway

    async def ws_ping(self, ws_connect: ClientWebSocketResponse, delay: float = 30.0):
        while True:
            self.logger.debug("websocket: ping!")
            await ws_connect.send_json({"s": 2, "sn": self.buffer["sn"]})
            self.logger.debug("sn:{}".format(self.buffer["sn"]))
            await asyncio.sleep(delay)

    async def ws_message(self, message: dict):
        if message["s"] == 0:
            # message
            self.buffer["sn"] += 1
        if message["s"] == 3:
            # pong
            self.logger.debug("websocket: pong!")

    async def websocket(self):
        async with self.session.ws_connect(self.gateway) as ws:
            self.logger.info("websocket: connected")
            self.broadcast.loop.create_task(self.ws_ping(ws))
            self.logger.info("websocket: ping tasks created")
            try:
                while True:
                    message = await ws.receive()
                    if message.type == WSMsgType.TEXT:
                        data = json.loads(message.data)
                        self.logger.debug("Received Data: " + str(data))
                        self.broadcast.loop.create_task(self.ws_message(data))
            except ValueError as e:
                print(e)

    async def main(self):
        await self.websocket()

    def launch(self):
        loop = self.broadcast.loop

        if not self.gateway:
            loop.run_until_complete(self.getGateway())

        try:
            loop.run_until_complete(self.main())
        finally:
            loop.run_until_complete(self.session.close())
