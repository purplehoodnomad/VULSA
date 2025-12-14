from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from src.domain.repositories.abstract import AbstractRepository
from .entity import User
from ..common.value_objects import UserId
from utils.enums import UserStatus


@dataclass(slots=True)
class UserFilterDto:
    offset: int
    limit: int
    status: Optional[UserStatus]


class AbstractUserRepository(AbstractRepository[User, UserId, UserFilterDto], ABC):
    pass