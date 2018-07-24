from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from projects.models import Project, ProjectMember, Invitation
from records.models import Record
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from braces.views import SelectRelatedMixin
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.core.files.storage import FileSystemStorage
from . import parse
# Create your views here.
from . import forms

import bibtexparser
from pylatexenc.latex2text import LatexNodes2Text
from pylatexenc.latexencode import utf8tolatex
import os
from mubm import settings


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

def edit_project_settings(request, slug):
    project = get_object_or_404(Project, slug=slug)

    form = forms.CreateProjectForm(request.POST or None, instance=project)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('projects:settings', slug=slug)
    return render(request, 'projects/project_edit.html', {'form':form, 'project':project})

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

def project_import_file(request, slug):
    project = get_object_or_404(Project, slug=slug)
    context = {'project':project}
    if request.method == 'POST' and request.FILES['import_file']:
        if request.FILES['import_file'].name.endswith('.bib'):
            importedfile = request.FILES['import_file']

            fs = FileSystemStorage()
            filename = fs.save('imported/'+project.slug+'/'+importedfile.name, importedfile)
            """
            Populate the project with the new records!
            """
            with open(os.path.join(settings.MEDIA_ROOT, filename)) as bibtex_file:
                bibtex_database = bibtexparser.load(bibtex_file)

            for entry in bibtex_database.entries:
                r = Record()
                r.entry_type = entry['ENTRYTYPE']
                r.cite_key = entry['ID']
                r.project = project
                fields = entry.items()
                for key, value in fields:
                    if key != 'ID' or key != 'ENTRYTYPE':
                        setattr(r, key, LatexNodes2Text().latex_to_text(value))
                r.save()

            os.remove(os.path.join(settings.MEDIA_ROOT, filename))
            return redirect('projects:single', slug=slug)
        else:
            pass
            # wrong file format

    return render(request, 'projects/project_import_file.html', context)



def list_projects(request):
    projects = Project.objects.filter(members=request.user)
    invites = Invitation.objects.filter(reciever=request.user)

    context = {
        'projects':projects,
        'invites':invites
    }
    return render(request, 'projects/project_list.html', context)

def delete_invite(request, slug, pk):
    try:
        invite = get_object_or_404(Invitation, pk=pk)
    except ObjectDoesNotExist:
        messages.warning(self.request, 'Warning: The invite could not be found and therefor not withdrawn')
    else:
        invite.delete()
    return redirect('projects:settings', slug=slug)

class LeaveProject(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args,**kwargs):
        return reverse('projects:all')

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=self.kwargs.get('slug'))
        user = request.user
        try:
            membership = get_object_or_404(ProjectMember, project=project, user=user)
        except ObjectDoesNotExist:
            messages.warning(self.request, 'Warning: You are not part of this group!')
        else:
            membership.delete()
        return super().get(request, *args,**kwargs)

class DeclineInvite(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args,**kwargs):
        return reverse('projects:all')

    def get(self, request, *args,**kwargs):
        project = get_object_or_404(Project, slug=self.kwargs.get('slug'))
        try:
            invite = get_object_or_404(Invitation, reciever=request.user, project=project)
        except ObjectDoesNotExist:
            messages.warning(self.request, 'Warning: The invite could not be found and therefor not deleted')
        else:
            invite.delete()
        return super().get(request, *args,**kwargs)

class JoinProject(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args,**kwargs):
        return reverse('projects:all')

    def get(self, request,*args,**kwargs):
        project = get_object_or_404(Project, slug=self.kwargs.get('slug'))

        try:
            ProjectMember.objects.create(user=self.request.user, project=project)
        except IntegrityError:
            messages.warning(self.request, 'Warning: You are already a member of this project!')
        else:
            messages.success(self.request, 'Invitation accepted!')
            invite = get_object_or_404(Invitation, reciever=request.user, project=project)
            invite.delete()

        return super().get(request, *args,**kwargs)

class DeleteProject(LoginRequiredMixin, generic.DeleteView):
    model = Project

    success_url = reverse_lazy('projects:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(members=self.request.user)

    def delete(self, *args, **kwargs):
        messages.success(self.request, 'Project Deleted')
        return super().delete(*args,**kwargs)
