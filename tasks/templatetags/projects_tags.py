from django import template

from tasks.models import Project

register = template.Library()

@register.simple_tag
def projects_list(user):
    projects = []
    if user.is_authenticated():
        projects = Project.objects.filter(user=user)

    return projects