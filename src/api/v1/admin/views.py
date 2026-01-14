from uuid import UUID

from fastapi import status, APIRouter, Depends
from fastapi.responses import JSONResponse

from usecase.admin import AbstractAddPermissionUseCase, AbstractRemovePermissionUseCase

from api.v1.dependencies import get_authentificated_user_id
from .dependencies import get_add_permission_usecase, get_remove_permission_usecase
from .schemas import EditPermissionSchema, RoleSchema
from usecase.admin.utils.dto import EditPermissionDTO


router = APIRouter(prefix="/admins")


@router.patch("/roles/add_permission", response_model=RoleSchema)
async def add_permission(
    payload: EditPermissionSchema,
    user_id: UUID = Depends(get_authentificated_user_id),
    usecase: AbstractAddPermissionUseCase = Depends(get_add_permission_usecase)
) -> JSONResponse:
    dto = EditPermissionDTO.from_schema(user_id, payload)
    role = await usecase.execute(dto)
    
    return JSONResponse(
        content=role.to_schema().model_dump(mode="json"),
        status_code=status.HTTP_200_OK
    )


@router.patch("/roles/remove_permission", response_model=RoleSchema)
async def remove_permission(
    payload: EditPermissionSchema,
    user_id: UUID = Depends(get_authentificated_user_id),
    usecase: AbstractRemovePermissionUseCase = Depends(get_remove_permission_usecase)
) -> JSONResponse:
    dto = EditPermissionDTO.from_schema(user_id, payload)
    role = await usecase.execute(dto)
    
    return JSONResponse(
        content=role.to_schema().model_dump(mode="json"),
        status_code=status.HTTP_200_OK
    )