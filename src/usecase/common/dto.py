from dataclasses import dataclass

from utils.enums import UserStatus


@dataclass(slots=True)
class UserCreateDTO:
    email: str
    password: str
    status: UserStatus