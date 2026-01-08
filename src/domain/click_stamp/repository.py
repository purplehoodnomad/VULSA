from abc import ABC, abstractmethod

from domain.repositories.abstract import AbstractRepository

from .entity import ClickStamp


class AbstractClickStampRepository(AbstractRepository[ClickStamp], ABC):
    pass