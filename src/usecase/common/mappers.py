from domain.link.entity import Link
from api.v1.link.schemas import LinkSchema

from domain.user.entity import User
from api.v1.user.schemas import UserSchema


def link_entity_to_schema(entity: Link) -> LinkSchema:
    return LinkSchema(
        link_id=entity.link_id.value,
        user_id=entity.user_id.value,
        long=entity.long.value,
        short=entity.short.value,
        times_used=entity.times_used,
        expires_at=entity.expires_at,
        is_active=entity.is_active,
        redirect_limit=entity.redirect_limit.value if entity.redirect_limit is not None else None,
        created_at=entity.created_at
    )


def user_entity_to_schema(entity: User) -> UserSchema:
    return UserSchema(
        user_id=entity.user_id.value,
        email=entity.email.value,
        status=entity.status,
        created_at=entity.created_at
    )