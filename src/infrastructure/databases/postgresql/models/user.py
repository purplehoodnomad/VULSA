# from typing import Optional
# from uuid import UUID, uuid4
# from datetime import datetime

# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from sqlalchemy import String, DateTime, func, Enum
# from sqlalchemy import UUID as UUIDAlchemy

# from ..base import Base

# from ....utils.enums import UserRole

# class User(Base):
#     __tablename__ = "user"

#     id: Mapped[UUID] = mapped_column(
#         UUIDAlchemy(as_uuid=True),
#         nullable=True, # временно
#         default=uuid4,
#         primary_key=True
#     )

#     email: Mapped[str] = mapped_column(
#         String(320),
#         nullable=False,
#         unique=True,
#         index=True
#     )

#     hashed_password: Mapped[str] = mapped_column(
#         String(1024),
#         nullable=False
#     )

#     role: Mapped[UserRole] = mapped_column(
#         Enum(UserRole),
#         nullable=False,
#         default=UserRole.USER
#     )

#     created_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         nullable=False,
#         server_default=func.now()
#     )

#     links: Mapped[list["Link"]] = relationship(back_populates="user")