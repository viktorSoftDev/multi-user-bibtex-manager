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
from django.forms.models import model_to_dict

# Create your views here.
from . import forms
from datetime import datetime
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from pylatexenc.latex2text import LatexNodes2Text
from pylatexenc.latexencode import utf8tolatex
import os
from django.conf import settings
from django.http import HttpResponse
from records import data
from django.contrib.auth.decorators import login_required
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
            pm = ProjectMember.objects.get_or_create(project=project, user=user, is_owner=True)[0]
            pm.save()
            return redirect('projects:single', slug=project.slug)


class SingleProject(LoginRequiredMixin, generic.DetailView):
    model = Project


@login_required
def project_settings(request, slug):
    project = Project.objects.get(slug=slug)
    invites = Invitation.objects.filter(project=project)
    memberships = project.memberships.all()
    context = {
        'project':project,
        'invites':invites,
        'memberships':memberships
    }
    template = 'projects/project_settings.html'
    return render(request, template, context)

@login_required
def edit_project_settings(request, slug):
    """
    Only admin
    """
    project = get_object_or_404(Project, slug=slug)

    form = forms.CreateProjectForm(request.POST or None, instance=project)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('projects:settings', slug=slug)
    return render(request, 'projects/project_edit.html', {'form':form, 'project':project})

@login_required
def project_invite(request, slug):
    """
    Only admin
    """
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
            setattr(inv, request.POST['permission'], True)
            inv.save()
            return redirect('projects:settings', slug=slug)

    form = forms.InviteForm(request.POST or None, initial={'permission': 'is_editor'})
    context['form'] = form
    template = 'projects/project_invite.html'
    return render(request, template, context)

@login_required
def project_import_file(request, slug):
    """
    Only admin and readwrite should be allowed to do this
    """
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
                    if key == 'ID' or key == 'ENTRYTYPE':
                        pass
                    else:
                        setattr(r, key, LatexNodes2Text().latex_to_text(value))
                r.save()

            os.remove(os.path.join(settings.MEDIA_ROOT, filename))
            return redirect('projects:single', slug=slug)
        else:
            pass
            # wrong file format

    return render(request, 'projects/project_import_file.html', context)


@login_required
def project_export_file(request, slug):
    project = get_object_or_404(Project, slug=slug)
    records = project.records.all()

    bib_database = BibDatabase()
    bib_database.entries = [None for x in range(records.count())]

    # create a dict with all entries
    i = 0
    for record in records: # iterating through all records
        entry_dict = {
            'ID':record.cite_key,
            'ENTRYTYPE':record.entry_type} # reading the ID and entry_type
        fields = model_to_dict(record).items()      # create a dict of the model data1
        for key, val in fields:             # iterate through the dict

            if key in data.FIELDS and (key != 'cite_key' or key != 'entry_type'):
                if val:
                    entry_dict[key] = utf8tolatex(val) # enter key and latex val
        bib_database.entries[i] = entry_dict       # populate the temp bib database
        i = i + 1
    # when done bib_database should contain all of the project's records
    # now create a string of it to write to file
    bib_string = bibtexparser.dumps(bib_database)
    fs = FileSystemStorage()
    with open(os.path.join(settings.MEDIA_ROOT, 'exported/'+ project.slug +'.bib'), 'w') as bibtex_file:
        bibtexparser.dump(bib_database, bibtex_file)

    """
        The following snippet was heavily inspired by the highest rated answer
        from this stackoverflow post
        https://stackoverflow.com/questions/36392510/django-download-a-file
    """
    file_path = os.path.join(settings.MEDIA_ROOT, 'exported/'+ project.slug +'.bib')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/bib")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

@login_required
def list_projects(request):
    projects = Project.objects.filter(members=request.user)
    invites = Invitation.objects.filter(reciever=request.user)

    context = {
        'projects':projects,
        'invites':invites
    }
    return render(request, 'projects/project_list.html', context)

@login_required
def delete_invite(request, slug, pk):
    """
    Only admin
    """
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
        invite = get_object_or_404(Invitation, reciever=request.user, project=project)
        try:
            ProjectMember.objects.create(user=self.request.user,
                                        project=project,
                                        is_owner=invite.is_owner,
                                        is_editor=invite.is_editor,
                                        is_reader=invite.is_reader)
        except IntegrityError:
            messages.warning(self.request, 'Warning: You are already a member of this project!')
        else:
            messages.success(self.request, 'Invitation accepted!')
            invite.delete()

        return super().get(request, *args,**kwargs)

class DeleteProject(LoginRequiredMixin, generic.DeleteView):
    """
    Only admin 
    """
    model = Project

    success_url = reverse_lazy('projects:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(members=self.request.user)

    def delete(self, *args, **kwargs):
        messages.success(self.request, 'Project Deleted')
        return super().delete(*args,**kwargs)
