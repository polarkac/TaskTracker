from django.views.generic import TemplateView, CreateView, DeleteView
from django.core.urlresolvers import reverse
from django.http import Http404

from tasks.models import Project, Task
from tasks.forms import ProjectForm

class ProjectDetailView(TemplateView):

    template_name = 'tasks/project_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        try:
            project = self.get_project()
        except Project.DoesNotExist:
            raise Http404
        tasks = self.get_tasks(project)

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

    def get_tasks(self, project):
        tasks = Task.objects.filter(project=project)
        print(tasks)

        return tasks

class ProjectCreateView(CreateView):

    model = Project
    template_name = 'tasks/project_form.html'
    form_class = ProjectForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})

        return kwargs

    def get_success_url(self):
        return reverse('tasks-project-detail', args=[self.object.id])

class ProjectDeleteView(DeleteView):

    model = Project
    template_name = 'tasks/project_delete_confirm.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        user = self.request.user
        try:
            obj = Project.objects.get(id=pk, user=user, default=False)
        except Project.DoesNotExist:
            raise Http404

        return obj

    def get_success_url(self):
        return reverse('tasks-project-detail', args=['general'])

class TaskCreateView(CreateView):

    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['name', 'priority', 'category']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({'project': self.get_project()})

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.project = self.get_project()
        self.object.save()

        return super().form_valid(form)

    def get_project(self):
        user = self.request.user
        try:
            project = Project.objects.get(
                pk=self.kwargs.get('project_pk'), user=user
            )
        except Project.DoesNotExist:
            raise Http404

        return project

    def get_success_url(self):
        return '/'
