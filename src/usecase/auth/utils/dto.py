from dataclasses import dataclass


@dataclass(slots=True)
class LoginUserDTO:
    email: str
    password: str