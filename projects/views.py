from django.views.generic import TemplateView, CreateView, DeleteView
from django.core.urlresolvers import reverse
from django.http import Http404

from projects.models import Project
from projects.forms import ProjectForm

class ProjectDetailView(TemplateView):

    template_name = 'projects/project_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        try:
            project = self.get_project()
        except Project.DoesNotExist:
            raise Http404
        tasks = self.get_tasks()

        context.update({'project': project, 'tasks': tasks})

        return context

    def get_project(self):
        user = self.request.user
        try:
            pk = int(self.kwargs.get('pk'))
            project = Project.objects.get(id=pk, user=user)
        except ValueError:
            project = None

        return project

    def get_tasks(self):
        return []

class ProjectCreateView(CreateView):

    model = Project
    template_name = 'projects/project_form.html'
    form_class = ProjectForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})

        return kwargs

    def get_success_url(self):
        return reverse('projects-list')

class ProjectDeleteView(DeleteView):

    model = Project
    template_name = 'projects/project_delete_confirm.html'

    def get_success_url(self):
        return reverse('projects-list')
