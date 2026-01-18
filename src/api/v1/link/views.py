from uuid import UUID

from fastapi import status, APIRouter, Depends
from fastapi.responses import JSONResponse, Response

from api.v1.dependencies import get_actor
from usecase.common.actor import Actor

from .schemas import LinkSchema, LinkCreateSchema, LinkListSchema, LinkListQueryParams, LinkUpdateSchema

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


router = APIRouter(prefix="/links")


@router.post("", response_model=LinkSchema)
async def create_short_link(
    payload: LinkCreateSchema,
    actor: Actor = Depends(get_actor),
    usecase: AbstractCreateLinkUseCase = Depends(get_link_create_usecase),
) -> JSONResponse:
    print(actor)
    dto = LinkCreateDTO.from_schema(actor, payload)
    link_dto = await usecase.execute(dto)
    
    return JSONResponse(
        content=link_dto.to_schema().model_dump(mode="json"),
        status_code=status.HTTP_201_CREATED
    )


@router.get("", response_model=LinkListSchema)
async def get_links_list(
    params: LinkListQueryParams = Depends(),
    actor: Actor = Depends(get_actor),
    usecase: AbstractGetLinksListUseCase = Depends(get_get_link_list_usecase)
) -> JSONResponse:
    actor.validate_actor_authentication()
    dto = LinkFilterDto.from_schema(actor, params)
    links = await usecase.execute(dto)
    links_schemas = [link.to_schema() for link in links]
    
    return JSONResponse(
        content=LinkListSchema(data=links_schemas).model_dump(mode="json"),
        status_code=status.HTTP_200_OK
    )


@router.delete("/{short}", response_model=None)
async def delete_short_link(
    short: str,
    actor: Actor = Depends(get_actor),
    usecase: AbstractDeleteShortUseCase = Depends(get_delete_short_usecase)
) -> Response:
    actor.validate_actor_authentication()
    await usecase.execute(actor=actor, short=short)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{short}", response_model=LinkSchema)
async def edit_short_link(
    short: str,
    payload: LinkUpdateSchema,
    actor: Actor = Depends(get_actor),
    usecase: AbstractEditShortLinkUseCase = Depends(get_edit_short_link_usecase)
) -> JSONResponse:
    actor.validate_actor_authentication()
    dto = LinkUpdateDTO.from_schema(actor, short, payload)
    link_dto = await usecase.execute(dto)

    return JSONResponse(
        content=link_dto.to_schema().model_dump(mode="json"),
        status_code=status.HTTP_200_OK
    )