from uuid import UUID

from fastapi import status, APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse

from domain.link.exceptions import LinkDoesNotExist, ShortLinkDoesNotExist #, ShortLinkAlreadyExists

from usecase.common.dto import UserCreateDTO
from usecase.user import CreateUserUsecase
from .dependencies import get_user_create_usecase
from .schemas import UserSchema, UserCreateSchema #, UserListSchema, UserListQueryParams 


router = APIRouter(prefix="/users")


@router.post("", response_model=UserSchema)
async def create_user(
    payload: UserCreateSchema,
    usecase: CreateUserUsecase = Depends(get_user_create_usecase),
) -> JSONResponse:
    
    dto = UserCreateDTO(
        email=str(payload.email),
        password=payload.password,
        status=payload.status
    )
    schema = await usecase.execute(dto)

    return JSONResponse(content=schema.model_dump(mode="json"), status_code=status.HTTP_201_CREATED)