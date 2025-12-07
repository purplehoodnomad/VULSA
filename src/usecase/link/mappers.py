from domain.link.entity import Link
from api.v1.link.schemas import LinkSchema

def to_schema(link: Link):
    return LinkSchema(
        link_id=link.link_id.value,
        user_id=link.user_id.value,
        long=link.long.value,
        short=link.short.value,
        times_used=link.times_used,
        expires_at=link.expires_at,
        is_active=link.is_active,
        redirect_limit=link.redirect_limit.value if link.redirect_limit is not None else None,
        created_at=link.created_at
    )