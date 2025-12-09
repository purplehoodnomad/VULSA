from uuid import UUID

from fastapi import status, APIRouter, Depends
from fastapi.responses import JSONResponse # RedirectResponse

from domain.link.exceptions import LinkDoesNotExist #, ShortLinkAlreadyExists

from usecase.link.dto import LinkCreateDTO
from usecase.link import (
    CreateLinkUsecase,
    GetLinkByIdUseCase
)
from infrastructure.di.injection import (
    get_link_create_usecase,
    get_link_get_by_id_usecase
)

from .schemas import LinkSchema, LinkCreateSchema


router = APIRouter(prefix="/links")


@router.post("", response_model=LinkSchema)
async def create_short_link(
    payload: LinkCreateSchema,
    usecase: CreateLinkUsecase = Depends(get_link_create_usecase),
) -> JSONResponse:
    
    dto = LinkCreateDTO(
        user_id=payload.user_id,
        long=str(payload.long),
        short = payload.short,
        expires_at=payload.expires_at,
        redirect_limit=payload.redirect_limit
    )
    link = await usecase.execute(dto)

    return JSONResponse(content=link.model_dump(mode="json"), status_code=status.HTTP_201_CREATED)


@router.get("/details/{url_id}", response_model=LinkSchema)
async def get_link_data(
    link_id: UUID,
    usecase: GetLinkByIdUseCase = Depends(get_link_get_by_id_usecase)
) -> JSONResponse:
    try:
        link = await usecase.execute(link_id)
    except LinkDoesNotExist:
        return JSONResponse(content="", status_code=status.HTTP_404_NOT_FOUND)

    return JSONResponse(content=link.model_dump(mode="json"), status_code=status.HTTP_200_OK)


# @router.get("", response_model=LinkListSchema)
# def get_links(pagination: Pagination = Depends(), repo: AbstractLinkRepository = Depends(get_link_repo),) -> JSONResponse:
#     try:
#         links = repo.list(limit=pagination.limit, offset=pagination.offset)
#     except LinkDoesNotExist:
#         return JSONResponse(content="", status_code=status.HTTP_404_NOT_FOUND)
    
#     links_schemas_list = []
#     for link in links:
#         links_schemas_list.append(LinkSchema(
#         owner_id=link.owner_id,
#         url_id=link.url_id,
#         base_url=link.base_url,
#         suffix=link.suffix,
#         expires_at=link.expires_at,
#         redirect_limit=link.redirect_limit,
#         times_used=link.times_used,
#         is_active=link.is_active,
#     ))
#     data = LinkListSchema(data=links_schemas_list)

#     return JSONResponse(content=data.model_dump(mode="json"), status_code=status.HTTP_200_OK)


# @router.get("/{suffix}")
# def process_redirect(suffix: str, repo: AbstractLinkRepository = Depends(get_link_repo),):
#     try:
#         link = repo.get_by_suffix(suffix)
#     except SuffixDoesNotExist:
#         return JSONResponse(content="", status_code=status.HTTP_404_NOT_FOUND)
    
#     if not link.is_active:
#         return JSONResponse(content="", status_code=status.HTTP_403_FORBIDDEN)
    
#     if link.expires_at is not None and link.expires_at < datetime.now(timezone.utc):
#         return JSONResponse(content="", status_code=status.HTTP_403_FORBIDDEN)
    
#     if link.redirect_limit is not None and link.redirect_limit <= link.times_used:
#         return JSONResponse(content="", status_code=status.HTTP_403_FORBIDDEN)
    
#     update_dto = link.consume_redirect()
#     repo.update(link.url_id, update_dto, wipe=False)

#     return RedirectResponse(url=link.base_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)



# @router.delete("/details/{url_id}")
# def delete_link(url_id: UUID, repo: AbstractLinkRepository = Depends(get_link_repo),) -> JSONResponse:
#     try:
#         repo.delete(url_id)
#         return JSONResponse(content="", status_code=status.HTTP_204_NO_CONTENT)
    
#     except LinkDoesNotExist:
#         return JSONResponse(content="", status_code=status.HTTP_404_NOT_FOUND)
    

# @router.put("/details/{url_id}", response_model=LinkSchema)
# def remake_link(url_id: UUID, payload: LinkUpdateSchema, repo: AbstractLinkRepository = Depends(get_link_repo),) -> JSONResponse:
#     dto = LinkUpdateDTO(owner_id=payload.owner_id, expires_at=payload.expires_at, redirect_limit=payload.redirect_limit)
#     try:
#         link = repo.update(url_id, dto, wipe=True)
#     except LinkDoesNotExist:
#         return JSONResponse(content="", status_code=status.HTTP_404_NOT_FOUND)

#     data = LinkSchema(
#         owner_id=link.owner_id,
#         url_id=link.url_id,
#         base_url=link.base_url,
#         suffix=link.suffix,
#         expires_at=link.expires_at,
#         redirect_limit=link.redirect_limit,
#         times_used=link.times_used,
#         is_active=link.is_active
#     )
#     return JSONResponse(content=data.model_dump(mode="json"), status_code=status.HTTP_200_OK)



# @router.patch("/details/{url_id}")
# def change_link(url_id: UUID, payload: LinkUpdateSchema, repo: AbstractLinkRepository = Depends(get_link_repo),) -> JSONResponse:
#     dto = LinkUpdateDTO(owner_id=payload.owner_id, expires_at=payload.expires_at, redirect_limit=payload.redirect_limit)
#     try:
#         link = repo.update(url_id, dto, wipe=False)
#     except LinkDoesNotExist:
#         return JSONResponse(content="", status_code=status.HTTP_404_NOT_FOUND)

#     data = LinkSchema(
#         owner_id=link.owner_id,
#         url_id=link.url_id,
#         base_url=link.base_url,
#         suffix=link.suffix,
#         expires_at=link.expires_at,
#         redirect_limit=link.redirect_limit,
#         times_used=link.times_used,
#         is_active=link.is_active
#     )
#     return JSONResponse(content=data.model_dump(mode="json"), status_code=status.HTTP_200_OK)