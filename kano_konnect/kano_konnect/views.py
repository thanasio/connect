from django.shortcuts import render_to_response
from django.template import RequestContext

from kano_konnect import tasks

__author__ = 'rogueleaderr'


def home(request):
    task = tasks.debug_task.delay()
    res = task.get()
    return render_to_response('homepage.html',
                              {
                                  "task_result": res,
                              },
                              context_instance=RequestContext(request))