from graia.broadcast.entities.dispatcher import BaseDispatcher
from graia.broadcast.interfaces.dispatcher import DispatcherInterface
from . import ApplicationDispatcher, KaiheilaEvent
from pydantic import Field
from ..group import Member, Group


class TextMessageEvent(KaiheilaEvent):
    type = "TextMessageEvent"
    text: str = Field(..., alias="content")
    sender: Member

    class Dispatcher(BaseDispatcher):
        mixin = [ApplicationDispatcher]

        @staticmethod
        async def catch(interface: DispatcherInterface):
            if interface.annotation is Member:
                return interface.event.sender
