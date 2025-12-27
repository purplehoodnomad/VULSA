from typing import Optional
from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, Enum
from sqlalchemy import UUID as UUIDAlchemy

from ..base import Base

from utils.enums import UserStatus

from domain.user.entity import User
from domain.value_objects.common import UserId
from domain.value_objects.user import Email, HashedPassword


class UserORM(Base):
    __tablename__ = "user"

    links: Mapped[list["LinkORM"]] = relationship(back_populates="user", cascade="all, delete, delete-orphan") # type: ignore
    tokens: Mapped[list["TokenORM"]] = relationship(back_populates="user", cascade="all, delete, delete-orphan") # type: ignore

    id: Mapped[UUID] = mapped_column(
        UUIDAlchemy(as_uuid=True),
        nullable=False,
        primary_key=True
    )

    email: Mapped[str] = mapped_column(
        String(320),
        nullable=False,
        unique=True,
        index=True
    )

    hashed_password: Mapped[str] = mapped_column(
        String(1024),
        nullable=False
    )

    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )


    @staticmethod
    def from_entity(link: User) -> "UserORM":
        return UserORM(
            id=link.user_id.value,
            email=link.email.value,
            hashed_password=link.hashed_password.value,
            status=link.status,
            created_at=link.created_at,
        )
    
    def to_entity(self):
        return User(
            user_id=UserId(self.id),
            email=Email(self.email),
            hashed_password=HashedPassword(self.hashed_password),
            status=self.status,
            created_at=self.created_at,
        )