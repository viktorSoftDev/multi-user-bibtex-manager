from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from projects.models import Project, ProjectMember
from django.shortcuts import get_object_or_404
from django.contrib import messages

from braces.views import SelectRelatedMixin
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)

# Create your views here.
from . import forms

class CreateProject(LoginRequiredMixin, generic.CreateView):
    form_class = forms.CreateProjectForm
    model = Project

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            project = form.save()
            user = self.request.user
            pm = ProjectMember.objects.get_or_create(project=project, user=user)[0]
            pm.save()
            return redirect('projects:single', project.slug)


class SingleProject(LoginRequiredMixin, generic.DetailView):
    model = Project

class ListProjects(LoginRequiredMixin, generic.ListView):
    model = Project

    def get_queryset(self):
        return Project.objects.filter(members=self.request.user)

class JoinProject(LoginRequiredMixin, generic.RedirectView):
    pass

class LeaveProject(LoginRequiredMixin, generic.RedirectView):
    pass
