import asyncio
from yarl import URL
from .utils import raise_for_return_code
from aiohttp import ClientSession

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

    def url_gen(self, path: str) -> str:
        return str(URL(self.baseURL) / "v3" / path)

    async def getGateway(self) -> str:
        async with self.session.get(self.url_gen("gateway/index")) as resp:
            resp.raise_for_status()
            data = await resp.json()
            raise_for_return_code(data)
            gateway = data["data"]["url"]
            self.gateway = gateway
            return gateway

    async def stop(self):
        await self.session.close()

    def launch(self):
        try:
            print(self.loop.run_until_complete(self.getGateway()))
        finally:
            self.loop.run_until_complete(self.stop())
