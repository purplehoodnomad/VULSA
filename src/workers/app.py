from celery import Celery
from celery.schedules import timedelta

from settings import settings


app = Celery(
    "VULSA",
    broker=settings.cache.get_url(1),
    backend=settings.cache.get_url(2),
)


app.autodiscover_tasks([
    "workers.sync_cache",
    # "workers.cleanup_links",
])


app.conf.beat_schedule = {
    "sync-cache-every-10-secs": {
        "task": "sync_links_cache",
        "schedule": timedelta(seconds=10)
    },
    # "cleanup-links-daily": {
    #     "task": "delete_expired_links",
    #     "schedule": 24 * 3600
    # },
}