from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from infrastructure.sqlalchemy.base import Base

from domain.role.entity import Role
from domain.value_objects.role import RoleName, RoleDescription



class RoleORM(Base):
    __tablename__ = "roles"

    users: Mapped[list["UserORM"]] = relationship(back_populates="roles") # type: ignore
    permissions: Mapped[list["PermissionORM"]] = relationship( # type: ignore
        "PermissionORM",
        secondary="role_permission_association",
        back_populates="roles"
    )

    
    name: Mapped[str] = mapped_column(
        String(255),
        primary_key=True,
        nullable=False,
    )

    description: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )


    @staticmethod
    def from_entity(entity: Role) -> "RoleORM":
        return RoleORM(
            name=entity.name.value,
            description=entity.description.value
        )
    
    # def update_from_entity(self, entity: Role) -> None:
    #     self.description = entity.description.value
    #     self.permissions = [permission.value for permission in entity._permissions]


    def to_entity(self) -> Role:
        return Role(
            name=RoleName(self.name),
            description=RoleDescription(self.description),
            permissions={permission.to_vo() for permission in self.permissions}
        )