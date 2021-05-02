class InvaildArgument(Exception):
    "缺少参数"
    pass


class InvaildToken(Exception):
    "无效的Token"
    pass


class FailedVerifyToken(Exception):
    "Token验证失败"
    pass


class ExpiredToken(Exception):
    "Token过期"
    pass
