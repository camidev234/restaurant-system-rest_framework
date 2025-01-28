from __future__ import absolute_import, unicode_literals

# Esto asegura que Celery esté disponible como parte del proyecto
from .celery import app as celery_app

__all__ = ('celery_app',)