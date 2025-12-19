from typing import Any
from sqlalchemy.exc import IntegrityError
from domain.user.exceptions import UserWithEmailAlreadyExistsException


PG_UNIQUE_VIOLATION = "23505"


_UNIQUE_CONSTRAINT_MAP = {
    "ix_user_email": {"attr": "email", "error": UserWithEmailAlreadyExistsException},
}

def handle_unique_integrity_error(
        error: IntegrityError,
        *,
        entity: Any
    ) -> None:
    """Maps PG_UNIQUE_VIOLATION to domain exceptions"""
    orig = error.orig

    if getattr(orig, "sqlstate", None) != PG_UNIQUE_VIOLATION:
        raise error

    for constraint, exc in _UNIQUE_CONSTRAINT_MAP.items():
        if constraint in str(orig):
            raise exc["error"](getattr(entity, exc["attr"]))

    raise error
