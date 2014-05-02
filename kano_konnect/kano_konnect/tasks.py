from __future__ import absolute_import

__author__ = 'rogueleaderr'

from celery import shared_task, task


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@task(bind=True)
def debug_task(self):
    return 'Request: {0!r}'.format(self.request)