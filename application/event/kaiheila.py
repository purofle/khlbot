from typing import Dict, Optional, Any
from graia.broadcast.entities.dispatcher import BaseDispatcher
from . import ApplicationDispatcher, EmptyDispatcher, KaiheilaEvent
from graia.broadcast.interfaces.dispatcher import DispatcherInterface
from ..group import Group, Member
from pydantic import Field, validator


class GroupMessage(KaiheilaEvent):
    type = "GroupMessage"

    target_id: int
    message: str = Field(..., alias="content")
    origin_extra: dict = Field(..., alias="extra")

    member: Optional[Group] = None
    group: Optional[Group] = None

    @validator("member", pre=True, always=True)
    def subject_handle_member(cls, v, values):
        return Member.parse_obj(values["origin_extra"]["author"])

    @validator("group", pre=True, always=True)
    def subject_handle_group(cls, v, values):
        return Group(id=values["target_id"])

    class Dispatcher(BaseDispatcher):
        mixin = [ApplicationDispatcher]

        @staticmethod
        async def catch(interface: DispatcherInterface):
            if interface.annotation is Member:
                return interface.event.member
            elif interface.annotation is Group:
                return interface.event.group
            elif interface.annotation is str:
                return interface.event.message

class PersonMessage(KaiheilaEvent):
    type = "PersonMessage"
    message: str = Field(..., alias="content")
    origin_extra: dict = Field(..., alias="extra")

    member: Optional[Member] = None

    @validator("member", pre=True, always=True)
    def subject_handle_group(cls, v, values):
        return Member.parse_obj(values["origin_extra"]["author"])

    class Dispatcher(BaseDispatcher):
        mixin = [ApplicationDispatcher]

        @staticmethod
        async def catch(interface: DispatcherInterface):
            if interface.annotation is Member:
                return interface.event.member
            elif interface.annotation is str:
                return interface.event.message


class guild_member_online(KaiheilaEvent):
    type = "guild_member_online"

    body: dict
    member: Optional[Member] = None

    @validator("member", pre=True, always=True)
    def subject_handle_user_id(cls, v, values):
        return Member(id=values["body"]["user_id"])

    class Dispatcher(BaseDispatcher):
        mixin = [ApplicationDispatcher]

        @staticmethod
        async def catch(interface: DispatcherInterface):
            if interface.annotation is Member:
                return interface.event.member
