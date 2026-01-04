from uuid import UUID

from fastapi import status, APIRouter, Depends
from fastapi.responses import JSONResponse, Response

from api.v1.dependencies import get_authentificated_user_id

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
    link_dto = await usecase.execute(dto)
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
    
    await usecase.execute(user_id=user_id, short=short)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{short}", response_model=LinkSchema)
async def edit_short_link(
    short: str,
    payload: LinkUpdateSchema,
    user_id: UUID = Depends(get_authentificated_user_id),
    usecase: AbstractEditShortLinkUseCase = Depends(get_edit_short_link_usecase)
) -> JSONResponse:
    dto = LinkUpdateDTO(
        long=str(payload.long) if payload.long is not None else None,
        new_short=payload.new_short,
        expires_at=payload.expires_at,
        redirect_limit=payload.redirect_limit,
        is_active=payload.is_active
    )
    link_dto = await usecase.execute(short=short, user_id=user_id, dto=dto)
    return JSONResponse(content=dto_to_schema(link_dto).model_dump(mode="json"), status_code=status.HTTP_200_OK)


