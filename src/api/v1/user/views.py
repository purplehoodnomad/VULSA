from uuid import UUID

from fastapi import status, APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from domain.user.exceptions import UserDoesNotExistException, UserWithEmailAlreadyExistsException

from usecase.common.dto import UserCreateDTO
from usecase.user import AbstractCreateUserUseCase
from .dependencies import get_user_create_usecase
from .schemas import UserSchema, UserCreateSchema


router = APIRouter(prefix="/users")


@router.post("", response_model=UserSchema)
async def create_user(
    payload: UserCreateSchema,
    usecase: AbstractCreateUserUseCase = Depends(get_user_create_usecase),
) -> JSONResponse:
    
    dto = UserCreateDTO(
        email=str(payload.email),
        password=payload.password,
        status=payload.status
    )
    try:
        schema = await usecase.execute(dto)
    except UserWithEmailAlreadyExistsException as e:
        raise HTTPException(detail=e.msg, status_code=status.HTTP_409_CONFLICT)

    return JSONResponse(content=schema.model_dump(mode="json"), status_code=status.HTTP_201_CREATED)


# @router.get("/{user_id}", response_model=UserSchema)
# async def get_user(
#     user_id: UUID,
#     usecase: AbstractGetUserUsecase = Depends(get_user_get_usecase),
# ) -> JSONResponse:
    
#     dto = UserCreateDTO(
#         email=str(payload.email),
#         password=payload.password,
#         status=payload.status
#     )
#     try:
#         schema = await usecase.execute(dto)
#     except UserWithEmailAlreadyExistsException as e:
#         raise HTTPException(detail=e.msg, status_code=status.HTTP_409_CONFLICT)

#     return JSONResponse(content=schema.model_dump(mode="json"), status_code=status.HTTP_201_CREATED)