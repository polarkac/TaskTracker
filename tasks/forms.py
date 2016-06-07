from django import forms
from django.utils.translation import ugettext as _
from django.db import transaction

from tasks.models import Project, Comment, TimeLog, TaskState

class ProjectForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_name(self):
        name = self.cleaned_data.get('name')

        try:
            Project.objects.get(name=name, user=self.user)
            raise forms.ValidationError(
                _('Project name is already exists.'), code='project-name-exists'
            )
        except Project.DoesNotExist:
            pass

        return name

    def save(self):
        project = super().save(commit=False)
        project.user = self.user
        project.save()

        return project

    class Meta:
        model = Project
        fields = ['name', 'description']

class CommentTimeLogForm(forms.Form):

    content = forms.CharField(widget=forms.Textarea(), required=False)
    spend_time = forms.IntegerField(initial=0, min_value=0, max_value=24 * 60)
    state = forms.ModelChoiceField(
        queryset=TaskState.objects.all(), empty_label=None
    )

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        spend_time = cleaned_data.get('spend_time')

        if content == '' and spend_time == 0:
            error_msg = _('You have to specify either comment or/and spend time.')
            self.add_error('content', error_msg)
            self.add_error('spend_time', error_msg)

    def save(self, task):
        with transaction.atomic():
            comment = Comment.objects.create(
                content=self.cleaned_data['content'],
                task=task
            )
            spend_time = self.cleaned_data['spend_time']
            if spend_time > 0:
                TimeLog.objects.create(spend_time=spend_time, comment=comment)
            if task.state != self.cleaned_data['state']:
                task.state = self.cleaned_data['state']
                task.save()
