# khlbot
## 介绍
一个简单的开黑啦bot的python实现.
## 使用例
```python
import asyncio
from kaiheila.application import KaiHeiLaApplication
from kaiheila.application.event.kaiheila import GroupMessage
from graia.broadcast import Broadcast
from kaiheila.application.group import Group, Member

loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
app = KaiHeiLaApplication(1/MTAyNTQ=/KzjLuKNLoZk3kRWrwR9JYQ==, bcc)

@bcc.receiver(GroupMessage)
async def groupevent(
        app: KaiHeiLaApplication,
        message: str,
        group: Group,
        member: Member):
    if message == hello:
        await app.sendGroupMessage(group, hello!)

app.launch()
```
执行这段代码，在任意一个*机器人有权利发送文字消息*的频道发送：`hello`后就会在频道内受到机器人的回复：`hello!`
## 感谢
- [`GraiaProject/Application`](https://github.com/GraiaProject/Application): 本框架大量参考这个项目，非常感谢
## 许可证
[`GNU AGPLv3`](/LICENSE)

