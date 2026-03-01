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
    "sync-cache-every-3-secs": {
        "task": "sync_links_cache",
        "schedule": timedelta(seconds=3)
    },
    "cleanup-links-in-hour": {
        "task": "delete_expired_links",
        "schedule": timedelta(seconds=3600)
    },
    "wipe-raw-clicks-in-10-min": {
        "task": "wipe_raw_clicks",
        "schedule": timedelta(seconds=10)
    }
}