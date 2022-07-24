import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tibia_Market.settings')

app = Celery('Tibia_Market')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "crawl_link": {
        "task": "scraper.tasks.get_link",
        "schedule": crontab(hour=11, minute=5),
    },
    "crawl_character": {
        "task": "scraper.tasks.collect_data",
        "schedule": timedelta(hours=12),
    },
    "crawl_character2": {
        "task": "scraper.tasks.collect_data",
        "schedule": crontab(hour=17, minute=5),
    }
}

app.conf.broker_url = 'redis://localhost:6379/0'
