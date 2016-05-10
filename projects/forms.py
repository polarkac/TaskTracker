from django import forms
from django.utils.translation import ugettext as _

from projects.models import Project

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
