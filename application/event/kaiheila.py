from graia.broadcast.entities.dispatcher import BaseDispatcher
from graia.broadcast.interfaces.dispatcher import DispatcherInterface
from . import ApplicationDispatcher, KaiheilaEvent
from pydantic import Field, validator
from ..group import Member, Group
import pdb


class TextMessageEvent(KaiheilaEvent):
    type = "TextMessageEvent"
    text: str = Field(..., alias="content")
    target_id: int
    member: Member

    class Dispatcher(BaseDispatcher):
        mixin = [ApplicationDispatcher]

        @staticmethod
        async def catch(interface: DispatcherInterface):
            if interface.annotation is Member:
                return interface.event.author
