from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy import UUID as UUIDAlchemy

from infrastructure.sqlalchemy.base import Base

from domain.token.entity import Token
from domain.value_objects.common import UserId
from domain.value_objects.token import TokenVO, TokenId


class TokenORM(Base):
    __tablename__ = "token"

    user: Mapped["UserORM"] = relationship("UserORM", back_populates="tokens", passive_deletes=True) # type: ignore
    
    id: Mapped[UUID] = mapped_column(
        UUIDAlchemy(as_uuid=True),
        primary_key=True,
        nullable=False,
    )
    
    user_id: Mapped[UUID] = mapped_column(
        UUIDAlchemy(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )

    access_token: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    refresh_token: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    access_token_expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    
    refresh_token_expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    @staticmethod
    def from_entity(entity: Token) -> "TokenORM":
        return TokenORM(
            id=entity.token_id.value,
            user_id=entity.user_id.value,
            access_token=entity.access_token.value,
            refresh_token=entity.refresh_token.value,
            access_token_expires_at=entity.access_token_expires_at,
            refresh_token_expires_at=entity.refresh_token_expires_at,
            created_at=entity.created_at,
        )
    
    def to_entity(self) -> Token:
        return Token(
            token_id=TokenId(self.id),
            user_id=UserId(self.user_id),
            access_token=TokenVO(self.access_token),
            refresh_token=TokenVO(self.refresh_token),
            access_token_expires_at=self.access_token_expires_at,
            refresh_token_expires_at=self.refresh_token_expires_at,
            created_at=self.created_at,
        )
    
    def update_from_entity(self, entity: Token) -> None:
        self.access_token = entity.access_token.value
        self.access_token_expires_at = entity.access_token_expires_at
        self.refresh_token = entity.refresh_token.value
        self.refresh_token_expires_at = entity.refresh_token_expires_at