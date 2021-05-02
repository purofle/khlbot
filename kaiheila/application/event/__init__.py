from graia.broadcast.entities.dispatcher import BaseDispatcher
from pydantic import validator
from graia.broadcast import BaseEvent
from graia.broadcast.interfaces.dispatcher import DispatcherInterface
from application.context import application


class KaiheilaEvent(BaseEvent):
    __base_event__ = True
    type: str

    @validator("type", allow_reuse=True)
    def type_limit(cls, v):
        if cls.type != v:
            raise Exception(
                "{0}'s type must be '{1}', not '{2}'".format(cls.__name__, cls.type, v)
            )
        return v

    class Config:
        extra = "ignore"

    class Dispatcher:
        pass


class ApplicationDispatcher(BaseDispatcher):
    @staticmethod
    async def catch(interface: DispatcherInterface):
        if getattr(interface.annotation, "__name__", None) == "KaiHeiLaApplication":
            return application.get()


class EmptyDispatcher(BaseDispatcher):
    mixin = [ApplicationDispatcher]

    @staticmethod
    async def catch(interface):
        pass
