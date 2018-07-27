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
        else:
            return redirect('projects:create')

def create_project(request):
    form = forms.CreateProjectForm(request.POST or None)
    template = 'projects/project_form.html'
    context = {
        'form':form,
    }

    if request.method == 'POST':
        if form.is_valid():
            project = form.save()
            user = request.user
            pm = ProjectMember.objects.get_or_create(project=project, user=user, is_owner=True)[0]
            pm.save()
            return redirect('projects:single', slug=project.slug)
    return render(request, template, context)






def project_detail(request, slug):
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        project = get_object_or_404(Project, slug=slug)

        records = Record.objects.filter(project=project)
        duplicates = []
        for record in records:
            if records.filter(cite_key=record.cite_key).count() > 1:
                duplicates.append(record)


        context = {
            'project':project,
            'userperm':project.memberships.get(user=request.user),
            'duplicates':duplicates,
            }
        template = 'projects/project_detail.html'
        return render(request, template, context)


@login_required
def project_settings(request, slug):
    """
    All members can access this view, template will ensure it only
    reveals availible views
    """
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        project = Project.objects.get(slug=slug)
        invites = Invitation.objects.filter(project=project)
        memberships = project.memberships.all()
        context = {
            'project':project,
            'invites':invites,
            'memberships':memberships,
            'userperm':project.memberships.get(user=request.user),
            'user':request.user,
        }
        template = 'projects/project_settings.html'
        return render(request, template, context)

@login_required
def edit_project_settings(request, slug):
    """
    Only admin can access this method
    """
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        project = get_object_or_404(Project, slug=slug)
        if ProjectMember.objects.get(user=request.user, project=project).is_owner:


            form = forms.CreateProjectForm(request.POST or None, instance=project)
            if request.method == 'POST':
                if form.is_valid():
                    form.save()
                    return redirect('projects:settings', slug=slug)
            return render(request, 'projects/project_edit.html', {'form':form, 'project':project})
        else:
            return HttpResponse("You don't have the permission to do this")


def edit_project_member(request, slug, pk):
    """
    Only admin
    """
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        user = User.objects.get(pk=pk)
        project = Project.objects.get(slug=slug)
        if ProjectMember.objects.get(user=request.user, project=project).is_owner:
            projectmember = ProjectMember.objects.get(user=user, project=project)
            if request.method == 'POST':
                form = forms.ProjectMemberForm(request.POST)
                if form.is_valid():
                    setattr(projectmember, 'is_owner', False)
                    setattr(projectmember, 'is_editor', False)
                    setattr(projectmember, 'is_reader', False)
                    setattr(projectmember, request.POST['permission'], True)
                    projectmember.save()
                    return redirect('projects:settings', slug=slug)

            if projectmember.is_owner:
                permission = 'is_owner'
            elif projectmember.is_editor:
                permission = 'is_editor'
            else:
                permission = 'is_reader'
            form = forms.ProjectMemberForm(request.POST or None, initial={'permission':permission})
            context = {
                'form':form,
                'projectmember':projectmember,
                'project':project,
                'user':request.user,
                'admins':ProjectMember.objects.filter(project=project, is_owner=True).count()
            }
            return render(request, 'projects/project_member_form.html', context)
        else:
            return HttpResponse("You don't have the permission to do this")

@login_required
def project_invite(request, slug):
    """
    Only admin can access this view
    """
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        project = Project.objects.get(slug=slug)
        if ProjectMember.objects.get(user=request.user, project=project).is_owner:
            context = {
                'project':project
            }

            if request.method == 'POST':
                form = forms.InviteForm(request.POST, project=project)
                if form.is_valid():
                    inv = Invitation()
                    inv.sender = request.user
                    inv.project = project
                    inv.reciever = User.objects.get(email=request.POST['email'])
                    inv.message = request.POST['message']
                    setattr(inv, request.POST['permission'], True)
                    inv.save()
                    return redirect('projects:settings', slug=slug)

            form = forms.InviteForm(request.POST or None, initial={'permission': 'is_editor'},  project=project)
            context['form'] = form
            template = 'projects/project_invite.html'
            return render(request, template, context)
        else:
            return HttpResponse("You don't have the permission to do this")

@login_required
def project_import_file(request, slug):
    """
    Only admin and readwrite should be allowed to do this
    """
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        project = get_object_or_404(Project, slug=slug)
        user = request.user
        pm = ProjectMember.objects.get(user=user, project=project)

        if pm.is_owner or pm.is_editor:
            form = forms.ImportFileForm(request.POST or None)
            context = {'project':project,
                        'form':form
                        }
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
                    context['error'] = "We currently only support .bib files, sorry"

            return render(request, 'projects/project_import_file.html', context)
        else:
            return HttpResponse("You don't have the permission to do this")

@login_required
def project_export_file(request, slug):
    """
    Letting all projectmembers be able to download file
    """
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
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
    Only admin can access this view
    """
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        if ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug)).is_owner:

            try:
                invite = get_object_or_404(Invitation, pk=pk)
            except ObjectDoesNotExist:
                messages.warning(self.request, 'Warning: The invite could not be found and therefor not withdrawn')
            else:
                invite.delete()
            return redirect('projects:settings', slug=slug)
        else:
            return HttpResponse("You don't have the permission to do this")

@login_required
def delete_member(request, slug, pk):
    """
    Only admin can delete members!
    """
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        if ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug)).is_owner:
            try:
                projectmember = get_object_or_404(ProjectMember, pk=pk)
            except ObjectDoesNotExist:
                messages.warning(self.request, 'Warning: The member could not be found and therefor not removed')
            else:
                projectmember.delete()
            return redirect('projects:settings', slug=slug)
        else:
            return HttpResponse("You don't have the permission to do this")


class LeaveProject(LoginRequiredMixin, generic.RedirectView):
    """
    All projectmembers can leave a project, should probably do a check to see
    that its not the only admin.
    """
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
    """
    Every user can access this view
    """
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
    """
    Every user can access this view
    """
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
    Only admin should be able to! How to ensure in this CBV? recreate a FBV?
    """
    model = Project

    success_url = reverse_lazy('projects:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(members=self.request.user)

    def delete(self, *args, **kwargs):
        messages.success(self.request, 'Project Deleted')
        return super().delete(*args,**kwargs)
