class DomainException(Exception):
    code = "DOMAIN_EXCEPTION"
    message = "Unknown Domain Exception"

    def __init__(self, message: str | None = None):
        if message is not None:
            self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message


class InvalidValue(DomainException):
    code = "INVALID_VALUE"
    message = "Some value is not valid"