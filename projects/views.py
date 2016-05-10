from django.views.generic import TemplateView, CreateView, DeleteView
from django.core.urlresolvers import reverse

from projects.models import Project
from projects.forms import ProjectForm

class ProjectsListView(TemplateView):

    template_name = 'projects/projects_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        projects = Project.objects.filter(user=self.request.user)
        context.update({'projects': projects})

        return context

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
