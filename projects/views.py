from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from projects.models import Project, ProjectMember, Invitation
from records.models import Record
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.forms.models import model_to_dict
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

"""
This is projects/views.py

This file contains the views related to a project
"""


@login_required
def create_project(request):
    """
    This view allows a user to create a new project
    """
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

@login_required
def project_detail(request, slug):
    """
    This view is availible to all project members
    This view contains the overview of a project including
    the datatable with all the records
    """
    # Try except to make sure the user is a member of this project
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        # User is not a member
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        # User is a member, details are provided and template is rendered.
        project = get_object_or_404(Project, slug=slug)
        records = Record.objects.filter(project=project)
        # If the project contains duplicates they are included in the response.
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
    All members can access this view
    """
    # Try except to make sure the user is a member of this project
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        # User is not a member
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        # User is a member
        project = Project.objects.get(slug=slug)
        invites = Invitation.objects.filter(project=project)
        memberships = project.memberships.all()
        context = {
            'project':project,
            'invites':invites,
            'memberships':memberships,
            'userperm':project.memberships.get(user=request.user),
            'user':request.user,
            'admins':project.memberships.filter(is_owner=True).count(),
        }
        template = 'projects/project_settings.html'
        return render(request, template, context)

@login_required
def edit_project_settings(request, slug):
    """
    Only admin can access this view
    Allows the admin to edit the project information
    """
    # Try except to make sure the user is a member of this project
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        # User is not a member
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        # User is a member,
        project = get_object_or_404(Project, slug=slug)
        # Access control, if not owner - access denied..
        if ProjectMember.objects.get(user=request.user, project=project).is_owner:
            # User has access
            form = forms.CreateProjectForm(request.POST or None, instance=project)
            if request.method == 'POST':
                # User submitted data
                if form.is_valid():
                    # form is valid - Save
                    form.save()
                    # slug could have been updated - make sure we redirect to the updated slug
                    slug = project.slug
                    return redirect('projects:settings', slug=slug)
            return render(request, 'projects/project_edit.html', {'form':form, 'project':project})
        else:
            # Access denied
            return HttpResponse("You don't have the permission to do this")

def edit_project_member(request, slug, pk):
    """
    This view is only available to the project admin.
    This view allows the admin to edit the details of a group member.
    """
    # Try except to make sure the user is a member of this project
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        # User is not a member
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        # User is a member,
        user = User.objects.get(pk=pk)
        project = Project.objects.get(slug=slug)

        # Access control, if not owner - access denied..
        if ProjectMember.objects.get(user=request.user, project=project).is_owner:
            projectmember = ProjectMember.objects.get(user=user, project=project)
            if request.method == 'POST':
                # User submitted data
                form = forms.ProjectMemberForm(request.POST)
                if form.is_valid():
                    # Form is valid, reset user permission and set the new. save.
                    setattr(projectmember, 'is_owner', False)
                    setattr(projectmember, 'is_editor', False)
                    setattr(projectmember, 'is_reader', False)
                    setattr(projectmember, request.POST['permission'], True)
                    projectmember.save()
                    # Redirect the user to the project settings page
                    return redirect('projects:settings', slug=slug)

            # this is used to fill the form with accurate data.
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
            # Access denied
            return HttpResponse("You don't have the permission to do this")

@login_required
def project_invite(request, slug):
    """
    This view is only available to the project admin.
    This view allows the admin to invite users to a project.
    """
    # Try except to make sure the user is a member of this project
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        # User is not a member
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        # User is a member,
        project = Project.objects.get(slug=slug)

        # Access control, if not owner - access denied..
        if ProjectMember.objects.get(user=request.user, project=project).is_owner:
            # User has access
            context = {
                'project':project
            }

            if request.method == 'POST':
                # User submitted data
                form = forms.InviteForm(request.POST, project=project)
                if form.is_valid():
                    # form is valid, create invitation and save
                    inv = Invitation()
                    inv.sender = request.user
                    inv.project = project
                    inv.reciever = User.objects.get(email=request.POST['email'])
                    inv.message = request.POST['message']
                    setattr(inv, request.POST['permission'], True)
                    inv.save()
                    # Send user back to the project settings page
                    return redirect('projects:settings', slug=slug)

            form = forms.InviteForm(request.POST or None, initial={'permission': 'is_editor'},  project=project)
            context['form'] = form
            template = 'projects/project_invite.html'
            return render(request, template, context)
        else:
            # Access denied
            return HttpResponse("You don't have the permission to do this")

@login_required
def project_import_file(request, slug):
    """
    This view is only available to project members with editing permissions
    This view allows the user to import a .bib file.
    """
    # Try except to make sure the user is a member of this project
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        # User is not a member
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        # User is a member,
        project = get_object_or_404(Project, slug=slug)
        user = request.user
        pm = ProjectMember.objects.get(user=user, project=project)

        # Access control, if not owner or editor - access denied..
        if pm.is_owner or pm.is_editor:
            form = forms.ImportFileForm(request.POST or None)
            context = {'project':project,
                        'form':form
                        }
            if request.method == 'POST' and request.FILES['import_file']:
                # user submitted data
                if request.FILES['import_file'].name.endswith('.bib'):
                    # the file is a .bib file
                    importedfile = request.FILES['import_file']
                    # save the file to the applications media storage
                    fs = FileSystemStorage()
                    filename = fs.save('imported/'+project.slug+'/'+importedfile.name, importedfile)
                    # Populate the project with the new records!
                    # open the file and read its content with bibtexparser
                    with open(os.path.join(settings.MEDIA_ROOT, filename)) as bibtex_file:
                        bibtex_database = bibtexparser.load(bibtex_file)

                    # iterate over each entry and save it
                    for entry in bibtex_database.entries:
                        r = Record()
                        r.entry_type = entry['ENTRYTYPE']
                        if entry['ID']:
                            r.cite_key = entry['ID']
                        r.project = project
                        fields = entry.items()
                        for key, value in fields:
                            if key == 'ID' or key == 'ENTRYTYPE':
                                pass # Already set.
                            else:
                                # set attribute, converted from LaTeX to unicode
                                setattr(r, key, LatexNodes2Text().latex_to_text(value))
                        r.save()

                    # When done, delete the imported file from the applications media storage
                    os.remove(os.path.join(settings.MEDIA_ROOT, filename))
                    # send user back to project detail page
                    return redirect('projects:single', slug=slug)
                else:
                    # file does not end with .bib
                    context['error'] = "We currently only support .bib files, sorry"

            return render(request, 'projects/project_import_file.html', context)
        else:
            # Access denied.
            return HttpResponse("You don't have the permission to do this")

@login_required
def project_export_file(request, slug):
    """
    This view is available to all project members.
    This view returns a file with the records of the project, in bibtex format
    """
    # Try except to make sure the user is a member of this project
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        # User is not a member
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        # User is a member,
        project = get_object_or_404(Project, slug=slug)
        records = project.records.all()

        # Create a bibdatabase object
        bib_database = BibDatabase()
        bib_database.entries = [None for x in range(records.count())]

        # create a dict with all entries
        i = 0
        for record in records:
            # iterating through all records

            # reading the ID and entry_type
            entry_dict = {
                'ID':record.cite_key,
                'ENTRYTYPE':record.entry_type}
            # create a dict of the model data
            fields = model_to_dict(record).items()
            for key, val in fields:
                # iterate through the dict
                if key in data.FIELDS and (key != 'cite_key' or key != 'entry_type'):
                    if val:
                        # enter key and convert from unicode to latex
                        entry_dict[key] = utf8tolatex(val)
            # populate the temp bib database
            bib_database.entries[i] = entry_dict
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
        # if something went wrong along the way
        raise Http404

@login_required
def list_projects(request):
    """
    This view displays all projects that a user is member of, including projects that
    the user is invited to
    """
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
    This view allows a project admin to delete an invite that has been sent to
    another user
    """
    # Try except to make sure the user is a member of this project
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        # User is not a member
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        # User is a member,

        # Access control, if not owner - access denied..
        if ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug)).is_owner:
            # User has access
            try:
                invite = get_object_or_404(Invitation, pk=pk)
            except ObjectDoesNotExist:
                messages.warning(self.request, 'Warning: The invite could not be found and therefor not withdrawn')
            else:
                invite.delete()
            return redirect('projects:settings', slug=slug)
        else:
            # Access denied..
            return HttpResponse("You don't have the permission to do this")

@login_required
def delete_member(request, slug, pk):
    """
    This view allows a project admin to remove members from the project.
    """
    # Try except to make sure the user is a member of this project
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        # User is not a member
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        # User is a member,

        # Access control, if not owner - access denied..
        if ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug)).is_owner:
            # User has access
            try:
                projectmember = get_object_or_404(ProjectMember, pk=pk)
            except ObjectDoesNotExist:
                messages.warning(self.request, 'Warning: The member could not be found and therefor not removed')
            else:
                projectmember.delete()
            return redirect('projects:settings', slug=slug)
        else:
            # Access denied...
            return HttpResponse("You don't have the permission to do this")

class LeaveProject(LoginRequiredMixin, generic.RedirectView):
    """
    This Class Based View allows a user to leave a project
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
    This Class Based View allows a user to decline an invitation to a project.
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
    This Class Based view allows a user to accept an invitation, making them a
    member of the project.
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

@login_required
def delete_project(request, slug):
    """
    This View allows a project admin to delete a project
    """
    # Try except to make sure the user is a member of this project
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        # User is not a member
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        # User is a member,
        # Acces control, if not owner - access denied..
        if ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug)).is_owner:
            # User has access
            try:
                project = get_object_or_404(Project, slug=slug)
            except ObjectDoesNotExist:
                messages.warning(self.request, 'Warning: The project could not be found and therefore not removed')
            else:
                project.delete()
            return redirect('projects:all')
        else:
            # access denied
            return HttpResponse("You don't have the permission to do this")
