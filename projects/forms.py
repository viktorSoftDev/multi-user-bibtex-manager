
from django import forms
from . import models

class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = ['project_title', 'description']
