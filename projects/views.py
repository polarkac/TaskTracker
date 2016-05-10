from django.views.generic import TemplateView

class ProjectsListView(TemplateView):

    template_name = 'projects/projects_list.html'
