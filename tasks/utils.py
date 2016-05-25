from django.db.models import Sum

from tasks.models import TimeLog

def get_total_project_spend_time(tasks):
    total_time = (
        TimeLog.objects.filter(comment__task__in=tasks)
        .aggregate(Sum('spend_time'))
    )['spend_time__sum']
    print(total_time)

    return total_time
