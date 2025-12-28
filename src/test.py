from domain.link.entity import Link
from domain.value_objects.common import UserId, LinkId
from domain.value_objects.link import *
from uuid import uuid4

Link.create(
    user_id=UserId(uuid4()),
    long=Long("https://google.com"),
    short=Short("aaaaaaaa"),
    redirect_limit=None
)