from dataclasses import dataclass
import validators


@dataclass(frozen=True)
class Email:
    """Represents email for User entity"""
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("Email is required")
        
        if not validators.email(self.value):
            raise ValueError(f"Invalid email: {self.value}")
    
    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class HashedPassword:
    """Represents hashed password for User entity"""
    value: str

    def __str__(self) -> str:
        return str(self.value)