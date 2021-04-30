from . import exceptions

code_exceptions_mapping = {
    40100: exceptions.InvaildArgument,
    40401: exceptions.InvaildToken,
    40102: exceptions.FailedVerifyToken,
    40103: exceptions.ExpiredToken,
}


def raise_for_return_code(code: dict):
    code = code.get("code")
    exception_code = code_exceptions_mapping.get(code)
    if exception_code:
        raise exception_code

type_map = {
        0: "TextMessageEvent"
        }
