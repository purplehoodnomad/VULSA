from sqlalchemy.exc import IntegrityError

from domain.user.exceptions import UserEmailAlreadyExists
from domain.link.exceptions import ShortLinkAlreadyExists


PG_UNIQUE_VIOLATION = "23505"


_UNIQUE_CONSTRAINT_MAP = {
    "ix_user_email": UserEmailAlreadyExists,
    "ix_link_short": ShortLinkAlreadyExists
}

def handle_unique_integrity_error(error: IntegrityError) -> None:
    """Maps PG_UNIQUE_VIOLATION to domain exceptions"""
    orig = error.orig

    if getattr(orig, "sqlstate", None) != PG_UNIQUE_VIOLATION:
        raise error

    for constraint, exc in _UNIQUE_CONSTRAINT_MAP.items():
        if constraint in str(orig):
            raise exc

    raise error
