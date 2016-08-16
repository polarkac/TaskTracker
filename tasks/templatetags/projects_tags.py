from django import template
from django.db.models import Prefetch

from tasks.models import Project, Task

register = template.Library()

@register.simple_tag
def projects_list(user):
    projects = []
    if user.is_authenticated():
        projects = Project.objects.filter(user=user).prefetch_related(
            Prefetch(
                'task_set', queryset=Task.objects.filter(paid=False),
                to_attr='unpaid_tasks'
            )
        )

    return projects
