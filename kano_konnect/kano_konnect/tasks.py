from __future__ import absolute_import

__author__ = 'rogueleaderr'

from celery import task

@task(bind=True)
def debug_task(self):
    return 'Request: {0!r}'.format(self.request)