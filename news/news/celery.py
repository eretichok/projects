import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news.settings')

app = Celery('news')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'weekly_send_mail': {
        'task': 'main.tasks.weekly_send_mail',
        'schedule': crontab(hour='8', day_of_week='sunday'),
        'args': (),
    },
}

app.conf.beat_schedule = {
    'new_post_mail': {
        'task': 'main.tasks.new_post_mail',
        'schedule': 5,
        'args': (),
    },
}
