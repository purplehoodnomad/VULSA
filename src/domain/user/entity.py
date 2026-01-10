from datetime import datetime

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from domain.link.entity import Link
from domain.value_objects.common import UserId
from domain.value_objects.user import Email, HashedPassword
from domain.value_objects.role import RoleName, Permission

from .exceptions import InvalidPassword, UserEmailMismatch, ShortLinkAccessDenied, NotAdminError


class User:
    """User entity"""
    _password_hasher = PasswordHasher()

    def __init__(
        self,
        *,
        user_id: UserId,
        email: Email,
        hashed_password: HashedPassword,
        role: RoleName,
        created_at: datetime
    ):
        self._user_id = user_id
        self._email = email
        self._hashed_password = hashed_password
        self._role = role
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
    def role(self) -> RoleName:
        return self._role
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    

    @staticmethod
    def create(*,
        email: Email,
        hashed_password: HashedPassword,
        role: RoleName
    ) -> "User":
        """Creates User entity"""
        user_id = UserId.generate()

        return User(
            user_id=user_id,
            email=email,
            hashed_password=hashed_password,
            role=role,
            created_at=datetime.now()
        )

    def change_password(self, plain_password: str) -> None:
        self._hashed_password = HashedPassword(self._password_hasher.hash(plain_password))

    def validate_password(self, plain_password: str) -> None:
        try:
            self._password_hasher.verify(self._hashed_password.value, plain_password)
        except VerifyMismatchError:
            raise InvalidPassword()
        
    def validate_email(self, email: Email) -> None:
        if email != self.email:
            raise UserEmailMismatch()
    
    def validate_link_ownership(self, entity: Link) -> None:
        if entity.user_id != self.user_id:
            raise ShortLinkAccessDenied()
    
    def validate_admin(self) -> None:
        if self.role.value != "admin":
            raise NotAdminError()