from dataclasses import dataclass
import validators

from domain.exceptions import InvalidValue


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if not self.value:
            raise InvalidValue("Email is required")
        
        if not validators.email(self.value):
            raise InvalidValue(f"Invalid email: {self.value}")
    
    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class HashedPassword:
    value: str

    def __str__(self) -> str:
        return str(self.value)