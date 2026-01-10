from usecase.admin.utils.dto import RoleDTO
from .schemas import RoleSchema

def dto_to_schema(dto: RoleDTO) -> RoleSchema:
    return RoleSchema(
        role_name=dto.name,
        description=dto.description,
        permissions=dto.permissions
    )