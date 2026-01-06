from dataclasses import dataclass
import secrets, string
import validators
from re import fullmatch

from domain.exceptions import InvalidValue


@dataclass(frozen=True)
class Long:
    value: str

    def __post_init__(self):
        if not self.value:
            raise InvalidValue("Link URL is required")
        
        if not validators.url(self.value):
            raise InvalidValue(f"Invalid URL: {self.value}")
    
    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Short:
    value: str

    MIN_SHORT_LINK_LENGTH = 2
    MAX_SHORT_LINK_LENGTH = 32

    @classmethod
    def generate(cls, length: int = MAX_SHORT_LINK_LENGTH) -> "Short":
        """
        Generates short link suffix of max available size by default.
        """
        size = cls.MAX_SHORT_LINK_LENGTH if length > cls.MAX_SHORT_LINK_LENGTH or length < cls.MIN_SHORT_LINK_LENGTH or length <= 0 else length
        return Short(''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(size)).lower())

    def __post_init__(self):
        if not self.value:
            raise InvalidValue("Suffix for short link is required")
        
        if not fullmatch(r'^[a-z0-9]+$', self.value):
            raise InvalidValue(f"Invalid short link: {self.value}")
    
    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class RedirectLimit:
    value: int | None

    def __post_init__(self):
        if self.value is not None and self.value <= 0:
            raise InvalidValue(f"Redirect limit must be positive integer: {self.value}")
    
    def __str__(self) -> str:
        return str(self.value)