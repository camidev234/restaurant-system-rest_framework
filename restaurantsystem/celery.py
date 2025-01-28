from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurantsystem.settings')

# Crea una instancia de Celery
app = Celery('restaurantsystem', broker='redis://localhost:6379/7')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(["orders.tasks.web_sockets"])

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')