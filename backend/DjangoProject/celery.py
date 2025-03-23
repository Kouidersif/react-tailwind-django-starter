import os
from django.conf import settings
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')

if settings.DEBUG:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'DjangoProject.settings'
elif not settings.DEBUG:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'DjangoProject.settings'


app = Celery('DjangoProject')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.update(
    beat_scheduler='django_celery_beat.schedulers:DatabaseScheduler'
)

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')