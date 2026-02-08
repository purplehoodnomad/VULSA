import pytest

from domain.value_objects.user import Email
from domain.exceptions import InvalidValue


def test_email_vo_validation():
    with pytest.raises(InvalidValue):
        Email("not-an-email")
