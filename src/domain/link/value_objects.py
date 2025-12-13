from dataclasses import dataclass
import secrets, string
import validators
from re import fullmatch

from src.config import MIN_SHORT_LINK_LENGTH, MAX_SHORT_LINK_LENGTH


@dataclass(frozen=True)
class Long:
    """Represents base URL for Link entity"""
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("Link URL is required")
        
        if not validators.url(self.value):
            raise ValueError(f"Invalid URL: {self.value}")
    
    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Short:
    """Represents shorten URL suffix for Link entity"""
    value: str

    @staticmethod
    def generate(len: int = MAX_SHORT_LINK_LENGTH) -> "Short":
        """
        Generates short link suffix of max available size by default.
        """
        size = MAX_SHORT_LINK_LENGTH if len > MAX_SHORT_LINK_LENGTH or len < MIN_SHORT_LINK_LENGTH or len <= 0 else len
        return Short(''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(size)).lower())

    def __post_init__(self):
        if not (MIN_SHORT_LINK_LENGTH <= len(self.value) <= MAX_SHORT_LINK_LENGTH):
            raise ValueError(f"Invalid short link length: {self.value}")
        
        if not fullmatch(r'^[a-z0-9]+$', self.value):
            raise ValueError(f"Invalid short link: {self.value}")
    
    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class RedirectLimit:
    """Represents shorten URL suffix for Link entity"""
    value: int

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError(f"Redirect limit must be positive integer: {self.value}")
    
    def __str__(self) -> str:
        return str(self.value)