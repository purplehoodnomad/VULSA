from abc import ABC
from dataclasses import dataclass
from typing import Optional

from utils.enums import UserStatus

from domain.repositories.abstract import AbstractRepository
from domain.value_objects.common import UserId

from .entity import User


@dataclass(slots=True)
class UserFilterDto:
    offset: int
    limit: int
    status: Optional[UserStatus]


class AbstractUserRepository(AbstractRepository[User, UserId, UserFilterDto], ABC):
    pass