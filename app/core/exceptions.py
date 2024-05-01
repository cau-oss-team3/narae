import logging
import sys
from fastapi import Request
from fastapi.responses import JSONResponse


logger = logging.getLogger("fastapi")


class CustomHTTPException(Exception):
    def __init__(self, status_code: int, err: str, headers: dict = None):
        super().__init__(err)
        self.status_code = status_code
        self.headers = headers
        self.err = err


class AuthenticationFailedException(CustomHTTPException):
    def __init__(self, status_code: int = 401, message: str = "Authentication failed"):
        super().__init__(status_code=status_code, err=message)


async def unhandled_custom_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    host = getattr(getattr(request, "client", None), "host", None)
    port = getattr(getattr(request, "client", None), "port", None)
    url = (
        f"{request.url.path}?{request.query_params}"
        if request.query_params
        else request.url.path
    )
    exception_type, exception_value, exception_traceback = sys.exc_info()
    exception_name = getattr(exception_type, "__name__", None)
    logger.warn(
        f"Custom exception: {exception_name}",
        extra={
            "host": host,
            "port": port,
            "url": url,
            "exception": exception_name,
            "exception_value": str(exception_value),
            "exception_traceback": exception_traceback,
        },
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"isSuccess": False, "err": exc.err},
    )
