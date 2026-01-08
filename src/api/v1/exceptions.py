from typing import cast

from fastapi import Request, status
from fastapi.responses import JSONResponse

from domain.exceptions import DomainException

DOMAIN_EXCEPTION_HTTP_STATUS: dict[str, int] = {
    "INVALID_VALUE": status.HTTP_400_BAD_REQUEST,

    "ACCESS_TOKEN_EXPIRED": status.HTTP_401_UNAUTHORIZED,
    "REFRESH_TOKEN_EXPIRED": status.HTTP_401_UNAUTHORIZED,

    "INVALID_PASSWORD": status.HTTP_403_FORBIDDEN,
    "USER_EMAIL_MISMATCH": status.HTTP_403_FORBIDDEN,
    "SHORT_LINK_ACCESS_DENIED": status.HTTP_403_FORBIDDEN,

    "USER_NOT_FOUND": status.HTTP_404_NOT_FOUND,
    "SHORT_LINK_NOT_FOUND": status.HTTP_404_NOT_FOUND,
    "USER_EMAIL_NOT_FOUND": status.HTTP_404_NOT_FOUND,
    "TOKEN_NOT_FOUND": status.HTTP_404_NOT_FOUND,

    "USER_EMAIL_ALREADY_EXISTS": status.HTTP_409_CONFLICT,
    "SHORT_LINK_ALREADY_EXISTS": status.HTTP_409_CONFLICT,
    
    "SHORT_LINK_EXPIRED": status.HTTP_410_GONE,
    "SHORT_LINK_REDIRECT_LIMIT_REACHED": status.HTTP_410_GONE,
    "SHORT_LINK_INACTIVE": status.HTTP_410_GONE
}

async def domain_exception_handler(
    request: Request,
    exc: Exception,
):
    domain_exc = cast(DomainException, exc)
    status_code = DOMAIN_EXCEPTION_HTTP_STATUS.get(domain_exc.code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JSONResponse(
        status_code=status_code,
        content={
            "error": domain_exc.code,
            "message": domain_exc.message,
        },
    )