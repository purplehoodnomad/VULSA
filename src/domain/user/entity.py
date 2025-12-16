from typing import Optional
from datetime import datetime

from utils.enums import UserStatus

from domain.value_objects.common import UserId
from domain.value_objects.user import Email, HashedPassword


class User:
    """User entity"""
    def __init__(
        self,
        *,
        user_id: UserId,
        email: Email,
        hashed_password: HashedPassword,
        status: UserStatus,
        created_at: datetime
    ):
        self._user_id = user_id
        self._email = email
        self._hashed_password = hashed_password
        self._status = status
        self._created_at = created_at


    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, User):
            return self.user_id == obj.user_id
        return False
    
    @property
    def user_id(self) -> UserId:
        return self._user_id
    
    @property
    def email(self) -> Email:
        return self._email
    
    @property
    def hashed_password(self) -> HashedPassword:
        return self._hashed_password
    
    @property
    def status(self) -> UserStatus:
        return self._status
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    

    @staticmethod
    def create(*,
        email: Email,
        hashed_password: HashedPassword,
        status: UserStatus = UserStatus.USER,
    ) -> "User":
        """Creates User entity"""
        user_id = UserId.generate()

        return User(
            user_id=user_id,
            email=email,
            hashed_password=hashed_password,
            status=status,
            created_at=datetime.now()
    )