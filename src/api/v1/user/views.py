from uuid import UUID

from fastapi import status, APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from domain.user.exceptions import UserDoesNotExistException, UserWithEmailAlreadyExistsException
from domain.value_objects.common import UserId
from domain.value_objects.token import Token as TokenVO

from usecase.user.utils.dto import UserCreateDTO, UserDeleteDTO
from usecase.user import (
    AbstractCreateUserUseCase,
    AbstractGetUserUseCase,
    AbstractDeleteUserUseCase,
    AbstractMeUseCase
)

from .dependencies import get_user_create_usecase, get_user_get_usecase, get_user_delete_usecase, get_me_usecase
from .schemas import UserSchema, UserCreateSchema, UserDeleteSchema
from .mappers import dto_to_schema


router = APIRouter(prefix="/users")

security_scheme = HTTPBearer(scheme_name="Bearer")


@router.post("", response_model=UserSchema)
async def create_user(
    payload: UserCreateSchema,
    usecase: AbstractCreateUserUseCase = Depends(get_user_create_usecase),
) -> JSONResponse:
    
    dto = UserCreateDTO(
        email=str(payload.email),
        password=payload.password,
    )
    try:
        created_user_dto = await usecase.execute(dto)
    except UserWithEmailAlreadyExistsException as e:
        raise HTTPException(detail=e.msg, status_code=status.HTTP_409_CONFLICT)
    
    schema = dto_to_schema(created_user_dto)

    return JSONResponse(content=schema.model_dump(mode="json"), status_code=status.HTTP_201_CREATED)


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(
    user_id: UUID,
    usecase: AbstractGetUserUseCase = Depends(get_user_get_usecase),
) -> JSONResponse:
    try:
        user = await usecase.execute(UserId(user_id))
    except UserDoesNotExistException as e:
        raise HTTPException(detail=e.msg, status_code=status.HTTP_404_NOT_FOUND)
    
    schema = dto_to_schema(user)

    return JSONResponse(content=schema.model_dump(mode="json"), status_code=status.HTTP_200_OK)


@router.delete("/{user_id}", response_model=UserSchema)
async def delete_user(
    user_id: UUID,
    payload: UserDeleteSchema,
    usecase: AbstractDeleteUserUseCase = Depends(get_user_delete_usecase),
) -> Response:
    dto = UserDeleteDTO(
        user_id=user_id,
        email=payload.email,
        password=payload.password
    )
    try:
        await usecase.execute(dto)
    except UserDoesNotExistException as e:
        raise HTTPException(detail=e.msg, status_code=status.HTTP_404_NOT_FOUND)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/me", response_model=UserSchema)
async def get_me(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    usecase: AbstractMeUseCase = Depends(get_me_usecase)
) -> JSONResponse:
    token_value = credentials.credentials
    try:    
        user = await usecase.execute(TokenVO(token_value))
    except UserDoesNotExistException as e:
        raise HTTPException(detail=e.msg, status_code=status.HTTP_404_NOT_FOUND)

    schema = dto_to_schema(user)

    return JSONResponse(content=schema.model_dump(mode="json"), status_code=status.HTTP_200_OK)