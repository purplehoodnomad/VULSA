from .schemas import LinkSchema
from usecase.link.utils.dto import LinkDTO

def dto_to_schema(dto: LinkDTO) -> LinkSchema:
    return LinkSchema(
        link_id=dto.link_id,
        user_id=dto.user_id,
        long=dto.long,
        short=dto.short,
        is_active=dto.is_active,
        expires_at=dto.expires_at,
        redirect_limit=dto.redirect_limit,
        created_at=dto.created_at,
        times_used=dto.times_used
    )