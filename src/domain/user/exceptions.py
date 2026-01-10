from domain.exceptions import DomainException


class UserNotFound(DomainException):
    code = "USER_NOT_FOUND"
    message = "User is not found"


class UserEmailAlreadyExists(DomainException):
    code = "USER_EMAIL_ALREADY_EXISTS"
    message = "User with this email already exists"


class UserEmailNotFound(DomainException):
    code = "USER_EMAIL_NOT_FOUND"
    message = "User with this email is not found"


class InvalidPassword(DomainException):
    code = "INVALID_PASSWORD"
    message = "User password is invalid"


class UserEmailMismatch(DomainException):
    code = "USER_EMAIL_MISMATCH"
    message = "Given email does not match user's" 


class ShortLinkAccessDenied(DomainException):
    code = "SHORT_LINK_ACCESS_DENIED"
    message = "Access to this short link is denied"

class NotAdminError(DomainException):
    code = "NOT_ADMIN_ERROR"
    message = "User has no admin role to perfrom request"