from uuid import UUID

from fastapi import status, APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse, Response

from api.v1.dependencies import get_authentificated_user_id

from domain.user.exceptions import LinkOwnershipViolation
from domain.link.exceptions import (
    ShortLinkDoesNotExistException,
    ShortLinkAlreadyExistsException,
)

from usecase.link.utils.dto import LinkCreateDTO, LinkUpdateDTO, LinkFilterDto
from usecase.link import (
    AbstractCreateLinkUseCase,
    AbstractDeleteShortUseCase,
    AbstractEditShortLinkUseCase,
    AbstractGetLinksListUseCase
)
    
from .dependencies import (
    get_link_create_usecase,
    get_get_link_list_usecase,
    get_delete_short_usecase,
    get_edit_short_link_usecase
)

from .schemas import LinkSchema, LinkCreateSchema, LinkListSchema, LinkListQueryParams, LinkUpdateSchema
from .mappers import dto_to_schema


router = APIRouter(prefix="/links")


@router.post("", response_model=LinkSchema)
async def create_short_link(
    payload: LinkCreateSchema,
    user_id: UUID = Depends(get_authentificated_user_id),
    usecase: AbstractCreateLinkUseCase = Depends(get_link_create_usecase),
) -> JSONResponse:
    dto = LinkCreateDTO(
        user_id=user_id,
        long=str(payload.long),
        short = payload.short,
        expires_at=payload.expires_at,
        redirect_limit=payload.redirect_limit
    )
    try:
        link_dto = await usecase.execute(dto)
    except ShortLinkAlreadyExistsException as e:
        raise HTTPException(detail=e.msg, status_code=status.HTTP_409_CONFLICT)
    except ValueError as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)

    return JSONResponse(content=dto_to_schema(link_dto).model_dump(mode="json"), status_code=status.HTTP_201_CREATED)


@router.get("", response_model=LinkListSchema)
async def get_links_list(
    params: LinkListQueryParams = Depends(),
    user_id: UUID = Depends(get_authentificated_user_id),
    usecase: AbstractGetLinksListUseCase = Depends(get_get_link_list_usecase)
) -> JSONResponse:
    
    dto = LinkFilterDto(
        offset=params.offset,
        limit=params.limit,
        user=user_id,
        older_than=params.older_than,
        newer_than=params.newer_than,
        active_status=params.active_status,
        has_expiration_date=params.has_expiration_date,
        has_redirect_limit=params.has_redirect_limit
    )

    links = await usecase.execute(dto)

    links_schemas = [dto_to_schema(link) for link in links]

    return JSONResponse(content=LinkListSchema(data=links_schemas).model_dump(mode="json"), status_code=status.HTTP_200_OK)


@router.delete("/{short}", response_model=None)
async def delete_short_link(
    short: str,
    user_id: UUID = Depends(get_authentificated_user_id),
    usecase: AbstractDeleteShortUseCase = Depends(get_delete_short_usecase)
) -> Response:
    
    try:
        await usecase.execute(user_id=user_id, short=short)
    except ShortLinkDoesNotExistException as e:
        raise HTTPException(detail=e.msg, status_code=status.HTTP_404_NOT_FOUND)
    except LinkOwnershipViolation as e:
        raise HTTPException(detail=e.msg, status_code=status.HTTP_403_FORBIDDEN)


    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{short}", response_model=LinkSchema)
async def edit_short_link(
    short: str,
    payload: LinkUpdateSchema,
    user_id: UUID = Depends(get_authentificated_user_id),
    usecase: AbstractEditShortLinkUseCase = Depends(get_edit_short_link_usecase)
) -> JSONResponse:
    dto = LinkUpdateDTO(
        long=str(payload.long),
        new_short=payload.new_short,
        expires_at=payload.expires_at,
        redirect_limit=payload.redirect_limit,
        is_active=payload.is_active
    )
    try:
        link_dto = await usecase.execute(short=short, user_id=user_id, dto=dto)
    except LinkOwnershipViolation as e:
        raise HTTPException(detail=e.msg, status_code=status.HTTP_403_FORBIDDEN)
    except ShortLinkDoesNotExistException as e:
        raise HTTPException(detail=e.msg, status_code=status.HTTP_404_NOT_FOUND)
    except ShortLinkAlreadyExistsException as e:
        raise HTTPException(detail=e.msg, status_code=status.HTTP_409_CONFLICT)
    except ValueError as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_409_CONFLICT)

    return JSONResponse(content=dto_to_schema(link_dto).model_dump(mode="json"), status_code=status.HTTP_200_OK)


