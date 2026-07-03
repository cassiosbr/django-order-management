import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')

# Ensure OpenTelemetry is initialized before Celery loads tasks.
import setup.otel  # noqa: F401

celery = Celery('setup')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()
