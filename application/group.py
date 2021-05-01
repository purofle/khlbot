"""[2021-05-01 01:58:21,610][DEBUG]: Received Data: {'s': 0, 'd': {'channel_type': 'GROUP', 'type': 1, 'target_id': '9324065608202891', 'author_id': '141191027', 'content': '草', 'extra': {'type': 1, 'guild_id': '5736598921010080', 'mention': [], 'mention_all': False, 'mention_roles': [], 'mention_here': False, 'author': {'id': '141191027', 'username': 'purofle', 'identify_num': '7385', 'online': True, 'os': 'Android', 'status': 1, 'avatar': 'https://img.kaiheila.cn/avatars/2021-04/4UCPtVFwH608c08c.jpg/icon', 'vip_avatar': 'https://img.kaiheila.cn/avatars/2021-04/4UCPtVFwH608c08c.jpg/icon', 'nickname': 'purofle', 'roles': [204278], 'is_vip': False}}, 'msg_id': '451f3986-ccc9-4eec-8f84-31df0ab3d279', 'msg_timestamp': 1619805501533,
'nonce': '1619805500295'}, 'extra': {'verifyToken': 'tj5709XxU4NrZkd0', 'encryptKey': '', 'callbackUrl': ''}, 'sn': 1}
"""

from pydantic import BaseModel


class Member(BaseModel):
    id: int


class Group(BaseModel):
    id: int
