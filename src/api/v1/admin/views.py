from uuid import UUID

from fastapi import status, APIRouter, Depends
from fastapi.responses import JSONResponse

from usecase.admin import AbstractAddPermissionUseCase, AbstractRemovePermissionUseCase

from api.v1.dependencies import get_authentificated_user_id
from .dependencies import get_add_permission_usecase, get_remove_permission_usecase
from .schemas import EditPermissionSchema, RoleSchema
from .mappers import dto_to_schema


router = APIRouter(prefix="/admins")


@router.patch("/roles/add_permission", response_model=RoleSchema)
async def add_permission(
    payload: EditPermissionSchema,
    user_id: UUID = Depends(get_authentificated_user_id),
    usecase: AbstractAddPermissionUseCase = Depends(get_add_permission_usecase)
) -> JSONResponse:
    role = await usecase.execute(user_id, payload.role, payload.permission)
    
    schema = dto_to_schema(role)
    return JSONResponse(content=schema.model_dump(mode="json"), status_code=status.HTTP_200_OK)

    
@router.patch("/roles/remove_permission", response_model=RoleSchema)
async def remove_permission(
    payload: EditPermissionSchema,
    user_id: UUID = Depends(get_authentificated_user_id),
    usecase: AbstractRemovePermissionUseCase = Depends(get_remove_permission_usecase)
) -> JSONResponse:
    role = await usecase.execute(user_id, payload.role, payload.permission)
    
    schema = dto_to_schema(role)
    return JSONResponse(content=schema.model_dump(mode="json"), status_code=status.HTTP_200_OK)