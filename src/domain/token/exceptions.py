from domain.exceptions import DomainException


class TokenNotFound(DomainException):
    code = "TOKEN_NOT_FOUND"
    message = "Token not found"


class AccessTokenExpired(DomainException):
    code = "ACCESS_TOKEN_EXPIRED"
    message = "Access token has expired"


class RefreshTokenExpired(DomainException):
    code = "REFRESH_TOKEN_EXPIRED"
    message = "Refresh token has expired"