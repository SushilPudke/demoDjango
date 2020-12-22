from __future__ import absolute_import, unicode_literals

import os
from dotenv import load_dotenv
from celery import Celery
from celery.schedules import crontab
from django.conf import settings


load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')

app = Celery('job_portal')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(settings.INSTALLED_APPS, related_name='tasks')

app.conf.beat_schedule = {
    'send_daily_users_report': {
        'task': 'accounts.tasks.daily_users_report',
        'schedule': crontab(minute=0, hour=0),
    },
    'send_weekly_users_report': {
        'task': 'accounts.tasks.weekly_users_report',
        'schedule': crontab(minute=0, hour=0, day_of_week='mon'),
    },
    'send_monthly_users_report': {
        'task': 'accounts.tasks.monthly_users_report',
        'schedule': crontab(minute=0, hour=0, day_of_month=1),
    },
    'send_year_users_report': {
        'task': 'accounts.tasks.year_users_report',
        'schedule': crontab(minute=0, hour=0, day_of_month=1, month_of_year=1),
    },
    'generate_sitemap': {
        'task': 'sitemap.tasks.generate_sitemap_task',
        'schedule': crontab(minute=0, hour=0),
    }
}
