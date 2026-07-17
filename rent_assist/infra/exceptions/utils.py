from fastapi import Request


def get_log_message(request: Request, exc: Exception, message: str | dict) -> str:
    url = f"{request.url.path}?{request.query_params}" if request.query_params else request.url.path
    exception_name = exc.__class__.__name__
    exception_value = str(exc)
    return f'"{request.method} {url}" <{exception_name}: {exception_value}> {message=}'


def loc_to_dot_sep(loc: tuple[str | int, ...]) -> str:
    path = ""
    for i, x in enumerate(loc):
        if isinstance(x, str):
            if i > 0:
                path += "."
            path += x
        elif isinstance(x, int):
            path += f"[{x}]"
        else:
            raise TypeError("Unexpected type")
    return path
