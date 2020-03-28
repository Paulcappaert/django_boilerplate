import os
from celery import Celery
from django.conf import settings
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

# set the default Django settings module for the 'celery' program and scanning for tasks.
app = Celery('mysite')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS, force=True)