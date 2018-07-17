from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from projects.models import Project, ProjectMember, Invitation
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from braces.views import SelectRelatedMixin
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)

# Create your views here.
from . import forms
from django.contrib.auth import get_user_model
User = get_user_model()

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
            return redirect('projects:single', slug=project.slug)


class SingleProject(LoginRequiredMixin, generic.DetailView):
    model = Project

def project_settings(request, slug):
    project = Project.objects.get(slug=slug)
    invites = Invitation.objects.filter(project=project)
    members = project.members.all()
    context = {
        'project':project,
        'members':members,
        'invites':invites
    }
    template = 'projects/project_settings.html'
    return render(request, template, context)

def project_invite(request, slug):
    project = Project.objects.get(slug=slug)
    context = {
        'project':project
    }

    if request.method == 'POST':
        form = forms.InviteForm(request.POST)
        if form.is_valid():
            inv = Invitation()
            inv.sender = request.user
            inv.project = project
            inv.reciever = User.objects.get(email=request.POST['email'])
            inv.message = request.POST['message']
            inv.save()
            return redirect('projects:settings', slug=slug)

    form = forms.InviteForm(request.POST or None)
    context['form'] = form
    template = 'projects/project_invite.html'
    return render(request, template, context)



class ListProjects(LoginRequiredMixin, generic.ListView):
    model = Project

    # this post method is only for deleting projects
    def post(self, request, *args, **kwargs):
        for k in request.POST.keys():
            if k != 'csrfmiddlewaretoken':
                Project.objects.filter(members=self.request.user, slug=k).delete()
        return redirect('projects:all')

    def get_queryset(self):
        return Project.objects.filter(members=self.request.user)

class JoinProject(LoginRequiredMixin, generic.RedirectView):
    pass

class LeaveProject(LoginRequiredMixin, generic.RedirectView):
    pass


class DeleteProject(LoginRequiredMixin, generic.DeleteView):
    model = Project

    success_url = reverse_lazy('projects:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(members=self.request.user)

    def delete(self, *args, **kwargs):
        messages.success(self.request, 'Project Deleted')
        return super().delete(*args,**kwargs)
