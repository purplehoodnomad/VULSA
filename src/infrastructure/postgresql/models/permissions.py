from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Table, Column, ForeignKey

from infrastructure.sqlalchemy.base import Base

from domain.value_objects.role import Permission


role_permission_association = Table(
    "role_permission_association",
    Base.metadata,
    Column("role_name", String(255), ForeignKey("roles.name"), primary_key=True),
    Column("permission_name", String(255), ForeignKey("permissions.name"), primary_key=True),
)


class PermissionORM(Base):
    __tablename__ = "permissions"

    roles: Mapped[list["RoleORM"]] = relationship( # type: ignore
        "RoleORM",
        secondary=role_permission_association,
        back_populates="permissions"
    )
    
    name: Mapped[str] = mapped_column(
        String(255),
        primary_key=True,
        nullable=False,
    )

    def to_vo(self) -> Permission:
        return Permission(self.name)