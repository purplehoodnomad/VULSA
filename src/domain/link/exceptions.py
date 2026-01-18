from domain.exceptions import DomainException


class ShortLinkAlreadyExists(DomainException):
    code = "SHORT_LINK_ALREADY_EXISTS"
    message = "Short link already exists"


class ShortLinkNotFound(DomainException):
    code = "SHORT_LINK_NOT_FOUND"
    message = "Short link not found"


class ShortLinkExpired(DomainException):
    code = "SHORT_LINK_EXPIRED"
    message = "Short link has expired"


class ShortLinkRedirectLimitReached(DomainException):
    code = "SHORT_LINK_REDIRECT_LIMIT_REACHED"
    message = "Maximum redirects reached for this short link"


class ShortLinkInactive(DomainException):
    code = "SHORT_LINK_INACTIVE"
    message = "Short link is temporarily deactivated by it's owner"


class AnonymousSessionNotFound(DomainException):
    code = "ANONYMOUS_SESSION_NOT_FOUND"
    message = "Anonymous session not found"