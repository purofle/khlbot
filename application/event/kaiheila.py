from graia.broadcast.entities.dispatcher import BaseDispatcher
from graia.broadcast.interfaces.dispatcher import DispatcherInterface
from . import KaiheilaEvent
from . import ApplicationDispatcher
from pydantic import Field


class TextMessageEvent(KaiheilaEvent):
    type = "TextMessageEvent"
    text: str = Field(..., alias="content")

    class Dispatcher(BaseDispatcher):
        mixin = [ApplicationDispatcher]

        @staticmethod
        async def catch(interface: DispatcherInterface):
            return "aaaaa"
