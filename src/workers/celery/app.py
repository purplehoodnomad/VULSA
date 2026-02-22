import logging
from celery import Celery
from celery.schedules import timedelta

from middleware import setup_logging
from settings import settings


setup_logging()
logger = logging.getLogger(__name__)

app = Celery(
    "VULSA",
    broker=settings.cache.get_url(1),
    backend=settings.cache.get_url(2),
)

app.autodiscover_tasks(["workers.celery.tasks"])


app.conf.beat_schedule = {
    "sync-cache-every-10-secs": {
        "task": "sync_links_cache",
        "schedule": timedelta(seconds=10)
    },
    "cleanup-links-daily": {
        "task": "delete_expired_links",
        "schedule": timedelta(seconds=10)
    }
}