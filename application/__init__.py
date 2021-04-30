import asyncio
import json
from typing import Optional

from aiohttp import ClientSession
from aiohttp.client_ws import ClientWebSocketResponse
from aiohttp.http_websocket import WSMsgType
from graia.broadcast import Broadcast
from graia.broadcast.builtin.event import BaseEvent
from graia.broadcast.utilles import run_always_await
from yarl import URL

import application.event.kaiheila

from . import logger
from .utils import raise_for_return_code, type_map
from .context import enter_context


class KaiHeiLaApplication:
    def __init__(
        self, token: str, broadcast: Broadcast, debug: bool = False
    ) -> None:
        self.broadcast = broadcast
        self.baseURL = "https://www.kaiheila.cn/api"
        self.token = token
        self.session = ClientSession(
            loop=broadcast.loop,
            headers={"Authorization": "Bot {}".format(self.token)},
        )
        self.gateway: str = ""
        self.logger = logger.LoggingLogger(
            **{"debug": True} if debug else {}
        )
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

    async def ws_ping(
        self, ws_connect: ClientWebSocketResponse, delay: float = 30.0
    ):
        while True:
            self.logger.debug("websocket: ping!")
            await ws_connect.send_json(
                {"s": 2, "sn": self.buffer["sn"]}
            )
            self.logger.debug("sn:{}".format(self.buffer["sn"]))
            await asyncio.sleep(delay)

    async def ws_message(self, message: dict):
        if message["s"] == 0:
            # message
            self.buffer["sn"] += 1
        if message["s"] == 3:
            # pong
            self.logger.debug("websocket: pong!")

    @staticmethod
    async def auto_parse_by_type(original_dict: dict) -> BaseEvent:
        event_int = int(original_dict.get("type"))
        event_type_str = type_map.get(event_int)
        if not event_type_str:
            raise ValueError("No such as event {}".format(event_int))
        event_type = Broadcast.findEvent(event_type_str)

        if not event_type:
            raise ValueError(
                "Cannot find event: {}".format(event_type_str)
            )

        return await run_always_await(
            event_type.parse_obj(
                {
                    k: v
                    for k, v in original_dict.items()
                    if k != "type"
                }
            )
        )

    async def websocket(self):
        async with self.session.ws_connect(self.gateway) as ws:
            self.logger.info("websocket: connected")
            ws_ping = self.broadcast.loop.create_task(
                self.ws_ping(ws)
            )
            self.logger.info("websocket: ping tasks created")
            try:
                while True:
                    message = await ws.receive()
                    if message.type == WSMsgType.TEXT:
                        data = json.loads(message.data)
                        self.logger.debug(
                            "Received Data: " + str(data)
                        )
                        self.broadcast.loop.create_task(
                            self.ws_message(data)
                        )

                        if data.get("d") and data.get("s") == 0:
                            event = await self.auto_parse_by_type(
                                data["d"]
                            )

                            with enter_context(app=self, event_i=event):
                                self.broadcast.postEvent(event)

            finally:
                ws_ping.cancel()

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
