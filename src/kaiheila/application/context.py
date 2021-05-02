from contextvars import ContextVar
from contextlib import contextmanager

application = ContextVar("application")
event = ContextVar("event")
event_loop = ContextVar("event_loop")
broadcast = ContextVar("broadcast")


@contextmanager
def enter_context(app=None, event_i=None):
    t1 = t2 = t3 = t4 = None
    if app:
        t1 = application.set(app)
        t3 = event_loop.set(app.broadcast.loop)
        t4 = broadcast.set(app.broadcast)
    if event_i:
        t2 = event.set(event_i)

    yield

    if t1:
        application.reset(t1)

    if all([t2, t3, t4]):
        event.reset(t2)
        event_loop.reset(t3)
        broadcast.reset(t4)
