from uuid import UUID

from fastapi import status, APIRouter, Depends
from fastapi.responses import JSONResponse, Response

from api.v1.dependencies import get_authentificated_user_id

from usecase.user.utils.dto import UserCreateDTO, UserDeleteDTO
from usecase.user import (
    AbstractCreateUserUseCase,
    AbstractGetUserByIdUseCase,
    AbstractDeleteUserUseCase,
)
from .dependencies import get_create_user_usecase, get_get_user_by_id_usecase, get_delete_user_usecase

from .schemas import UserSchema, UserCreateSchema, UserDeleteSchema
from .mappers import dto_to_schema


router = APIRouter(prefix="/users")


@router.post("", response_model=UserSchema)
async def create_user(
    payload: UserCreateSchema,
    usecase: AbstractCreateUserUseCase = Depends(get_create_user_usecase),
) -> JSONResponse:
    
    dto = UserCreateDTO(
        email=str(payload.email),
        password=payload.password,
        role=payload.role
    )
    created_user_dto = await usecase.execute(dto)
    
    schema = dto_to_schema(created_user_dto)

    return JSONResponse(content=schema.model_dump(mode="json"), status_code=status.HTTP_201_CREATED)


@router.get("/me", response_model=UserSchema)
async def get_me(
    user_id: UUID = Depends(get_authentificated_user_id),
    usecase: AbstractGetUserByIdUseCase = Depends(get_get_user_by_id_usecase)
) -> JSONResponse:
    user = await usecase.execute(user_id)
    schema = dto_to_schema(user)
    
    return JSONResponse(content=schema.model_dump(mode="json"), status_code=status.HTTP_200_OK)


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(
    user_id: UUID,
    usecase: AbstractGetUserByIdUseCase = Depends(get_get_user_by_id_usecase),
) -> JSONResponse:
    user = await usecase.execute(user_id)
    
    schema = dto_to_schema(user)
    return JSONResponse(content=schema.model_dump(mode="json"), status_code=status.HTTP_200_OK)


@router.delete("/{user_id}", response_model=UserSchema)
async def delete_user(
    user_id: UUID,
    payload: UserDeleteSchema,
    usecase: AbstractDeleteUserUseCase = Depends(get_delete_user_usecase),
) -> Response:
    dto = UserDeleteDTO(
        user_id=user_id,
        email=payload.email,
        password=payload.password
    )
    await usecase.execute(dto)
    return Response(status_code=status.HTTP_204_NO_CONTENT)