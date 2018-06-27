from django.shortcuts import render
from django.ursl import reverse
from django.views import generic
from projects.models import Project, ProjectMember
from django.shortcuts import get_object_or_404
from django.contrib import messages

from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)

# Create your views here.


class CreateProject(LoginRequiredMixin, generic.CreateView):
    fields = ('project_title','description','members')
    model = Project

class SingleProject(LoginRequiredMixin, generic.DetailView):
    model = Project

class ListProjects(LoginRequiredMixin, generic.ListView):
    model = Project

class JoinProject(LoginRequiredMixin, generic.RedirectView):
    pass

class LeaveProject(LoginRequiredMixin, generic.RedirectView):
    pass
