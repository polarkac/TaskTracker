from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin

from tasks.models import TimeLog

def get_total_project_spend_time(tasks):
    unpaid_tasks = tasks.filter(paid=False)
    total_time = (
        TimeLog.objects.filter(comment__task__in=unpaid_tasks)
        .aggregate(Sum('spend_time'))
    )['spend_time__sum']

    return total_time

def annotate_total_time_per_task(tasks):
    total_times = {}
    times = (
        TimeLog.objects.filter(comment__task__in=tasks).values('comment__task')
        .annotate(Sum('spend_time'))
    )
    for time in times:
        total_times.update({time['comment__task']: time['spend_time__sum']})

    for task in tasks:
        task.total_spend_time = total_times.get(task.id, 0)

class LoginRequired(LoginRequiredMixin):

    redirect_field_name = None
