from typing import Optional
from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, Enum, ForeignKey
from sqlalchemy import UUID as UUIDAlchemy

from infrastructure.sqlalchemy.base import Base

from utils.enums import UserStatus

from domain.user.entity import User
from domain.value_objects.common import UserId
from domain.value_objects.user import Email, HashedPassword
from domain.value_objects.role import RoleName


class UserORM(Base):
    __tablename__ = "user"

    links: Mapped[list["LinkORM"]] = relationship(back_populates="user", cascade="all, delete, delete-orphan") # type: ignore
    tokens: Mapped[list["TokenORM"]] = relationship(back_populates="user", cascade="all, delete, delete-orphan") # type: ignore
    roles: Mapped["RoleORM"] = relationship("RoleORM", back_populates="users") # type: ignore

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

    role: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("roles.name"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )


    @staticmethod
    def from_entity(entity: User) -> "UserORM":
        return UserORM(
            id=entity.user_id.value,
            email=entity.email.value,
            hashed_password=entity.hashed_password.value,
            role=entity.role.value,
            created_at=entity.created_at,
        )
    
    def to_entity(self):
        return User(
            user_id=UserId(self.id),
            email=Email(self.email),
            hashed_password=HashedPassword(self.hashed_password),
            role=RoleName(self.role),
            created_at=self.created_at,
        )