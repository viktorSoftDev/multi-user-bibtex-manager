from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from records.data import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import pytz
from projects.models import ProjectMember, Project
from . import models
from . import forms
from django.contrib.auth import get_user_model
User = get_user_model()

"""
This is: records/views.py

This file contains all record specific views.
"""

@login_required
def record_detail(request, slug, pk):
    """
    This view is accessible for all project members.
    Straight forward; Displays a single record.
    """
    # Try except to make sure the user is a member of this project
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        # User is not a member
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        # User is a member, details are provided and template is rendered.
        record = get_object_or_404(models.Record, pk=pk)
        project = models.Project.objects.get(slug=slug)
        template = 'records/record_detail.html'
        data = forms.ShowRecordForm(data=model_to_dict(record), entry=record.entry_type)
        context = {
            'record':record,
            'project':project,
            'userperm':project.memberships.get(user=request.user),
            'data':data
        }
        return render(request,template,context)

@login_required
def clone_record(request, slug, pk):
    """
    This view is only available for projectmembers with editing permissions.
    This view returns forms with data from requested record and saves submitted
    data into a new record object.
    """
    # Try except to make sure the user is a member of this project
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        # User is not a member.
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        # User is a member,
        project = get_object_or_404(models.Project, slug=slug)
        record = get_object_or_404(models.Record, pk=pk)
        pm = ProjectMember.objects.get(user=request.user, project=project)

        # Access control.. if not owner or editor - access denied.
        if pm.is_owner or pm.is_editor:
            # User has access..
            if request.method == 'POST':
                # User has submitted the form.
                form1 = forms.GeneralRecordForm(request.POST)
                form2 = forms.SpecificRecordForm(request.POST, entry=request.POST['entry_type'])
                if form1.is_valid() and form2.is_valid():
                    # Save data in a new record
                    data1 = form1.clean()
                    data2 = form2.clean()
                    record.entry_type = data1['entry_type']
                    record.cite_key = data1['cite_key']
                    record.last_edited = timezone.now()
                    record.save()
                    # Send user back to project detail, the overview of all records in the project.
                    return redirect('projects:single', slug=slug)

            else:
                # Form is filled in with the data from previous record
                form1 = forms.GeneralRecordForm(data=model_to_dict(record))
                form2 = forms.SpecificRecordForm(data=model_to_dict(record),entry=record.entry_type)
                context = {
                    'form1':form1,
                    'project':project,
                    'form2':form2,
                }
                return render(request, 'records/record_copy.html', context)
        else:
            # Access denied...
            return HttpResponse("You don't have the permission to do this")

@login_required
def record_conflict(request, slug, pk):
    """
    This view is only available for projectmembers with editing permissions.
    This view handles the logic necessary to resolve an editing conflict.
    The view does not render any template.
    """
    # Try except to make sure the user is a member of this project
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        # User is not a member.
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        # User is a member,
        project = Project.objects.get(slug=slug)
        if request.method == 'POST':
            # User has decided which record(s) to keep
            if request.POST['keep'] == 'OLD':
                # old is already saved, just dont save the new one
                return redirect('projects:single', slug=slug)
            elif request.POST['keep'] == 'NEW':
                # delete old and save new!
                record = get_object_or_404(models.Record, pk=pk)
            # User has decided to save both or the new one
            form1 = forms.GeneralRecordForm(request.POST)
            form2 = forms.SpecificRecordForm(request.POST, entry=request.POST['entry_type'])
            context = {
                'form1':form1,
                'project':project,
                'form':form2,
                }
            if form2.is_valid() and form1.is_valid():
                fields = [f.name for f in models.Record._meta.get_fields()]
                data1 = form1.clean()
                data2 = form2.clean()
                # Additional form validation.
                if data1['entry_type'] == 'book':
                    if data2['author']== '' and data2['editor'] == '':
                        context['err'] = True
                        context['errmessage'] = "Fill in either Author or Editor"
                        return render(request, 'records/record_form.html', context)
                elif data1['entry_type'] == 'inbook':
                    if data2['author'] == '' and data2['editor'] == '':
                        context['err'] = True
                        context['errmessage'] = "Fill in either Author or Editor"
                        return render(request, 'records/record_form.html', context)
                    elif data2['chapter'] == '' and data2['pages'] == '':
                        context['err'] = True
                        context['errmessage'] = "Fill in either Chapter or Pages"
                        return render(request, 'records/record_form.html', context)
                # Form is valid .. save into new record
                record.entry_type = data1['entry_type']
                record.cite_key = data1['cite_key']
                record.project = project
                for fieldname in fields:
                    if fieldname in data2:
                        setattr(record, fieldname, data2[fieldname])
                record.last_edited = timezone.now()
                record.save()
            else:
                # form is not valid
                context['err'] = True
                return render(request, 'records/record_form.html', context)
            # Send user back to project detail, the overview of all records in the project.
            return redirect('projects:single', slug=slug)

@login_required
def edit_record(request, slug, pk):
    """
    This view is only available for projectmembers with editing permissions.
    This view handles the editing of existing records.
    """
    # Try except to make sure the user is a member of this project
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        # User is not a member.
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        # User is a member,
        project = get_object_or_404(models.Project, slug=slug)
        record = get_object_or_404(models.Record, pk=pk)
        pm = ProjectMember.objects.get(user=request.user, project=project)

        # Access control.. if not owner or editor - access denied.
        if pm.is_owner or pm.is_editor:
            # User has access
            if request.method == 'POST':
                # User submits data
                form1 = forms.GeneralRecordForm(request.POST)
                form2 = forms.SpecificRecordForm(request.POST, entry=request.POST['entry_type'])
                context = {
                    'form1':form1,
                    'project':project,
                    'form':form2,
                    }
                if form2.is_valid() and form1.is_valid():
                    fields = [f.name for f in models.Record._meta.get_fields()]
                    data1 = form1.clean()
                    data2 = form2.clean()
                    # Additional form validation.
                    if data1['entry_type'] == 'book':
                        if data2['author']== '' and data2['editor'] == '':
                            context['err'] = True
                            context['errmessage'] = "Fill in either Author or Editor"
                            return render(request, 'records/record_edit.html', context)
                    elif data1['entry_type'] == 'inbook':
                        if data2['author'] == '' and data2['editor'] == '':
                            context['err'] = True
                            context['errmessage'] = "Fill in either Author or Editor"
                            return render(request, 'records/record_edit.html', context)
                        elif data2['chapter'] == '' and data2['pages'] == '':
                            context['err'] = True
                            context['errmessage'] = "Fill in either Chapter or Pages"
                            return render(request, 'records/record_edit.html', context)
                    # Form is valid .. save into new record
                    # making sure no one has edited the record while session is running
                    if record.last_edited.__str__() == request.COOKIES.get('last_edited'):
                        # No conflict, go on save changes.
                        record.entry_type = data1['entry_type']
                        record.cite_key = data1['cite_key']
                        record.project = project
                        for fieldname in fields:
                            if fieldname in data2:
                                setattr(record, fieldname, data2[fieldname])
                        record.last_edited = timezone.now()
                        record.save()
                        # Send user back to project detail, the overview of all records in the project.
                        return redirect('projects:single', slug=slug)
                    else:
                        # someone changed the record before the user managed to save
                        data = forms.ShowRecordForm(data=model_to_dict(record), entry=record.entry_type)
                        context = {
                            'old_record':record,
                            'form1':form1,
                            'project':project,
                            'form':form2,
                            'data':data
                        }
                        # send user to the conflict page.
                        return render(request, 'records/record_conflict.html', context)

                else:
                    # Form is not valid
                    context = {
                        'form1':form1,
                        'project':project,
                        'form':form2,
                        'err':True
                    }
                    return render(request, 'records/record_edit.html', context)
            else:
                # User hasn't submitted any data yet
                # Form filled in with data for selected record.
                form1 = forms.GeneralRecordForm(data=model_to_dict(record))
                form2 = forms.SpecificRecordForm(data=model_to_dict(record),entry=record.entry_type)
                context = {
                    'form1':form1,
                    'form2':form2,
                    'project':project,
                    'record':record
                }
                # Create response in order to set cookie
                response = render(request, 'records/record_edit.html', context)
                # set cookie to enable later check for conlfict
                response.set_cookie('last_edited', record.last_edited.__str__())
                return response
        else:
            # Access denied.
            return HttpResponse("You don't have the permission to do this")

@login_required
def delete_record(request, slug, pk):
    """
    This view is only available for projectmembers with editing permissions.
    This view handles logic to delete a specific record
    """
    # Try except to make sure the user is a member of this project
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        # User is not a member
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        # User is a member
        pm = ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
        # Access control.. if not owner or editor - access denied.
        if pm.is_owner or pm.is_editor:
            # User has access
            record = get_object_or_404(models.Record, pk=pk)
            # Delete record
            models.Record.objects.filter(project=get_object_or_404(models.Project, slug=slug), pk=pk).delete()
            # Send user back to project detail, the overview of all records in the project.
            return redirect('projects:single', slug=slug)
        else:
            # Access denied...
            return HttpResponse("You don't have the permission to do this")

@login_required
def create_record(request, slug):
    """
    This view is only available for projectmembers with editing permissions.
    This view handles logic to create a new record
    """
    # Try except to make sure the user is a member of this project
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        # User is not a member
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        # User is a member
        project = get_object_or_404(models.Project, slug=slug)
        form1 = forms.GeneralRecordForm(request.POST or None)
        pm = ProjectMember.objects.get(user=request.user, project=project)

        # Access control.. if not owner or editor - access denied.
        if pm.is_owner or pm.is_editor:
            # User has access
            if request.method == 'POST':
                # User submits data
                form1 = forms.GeneralRecordForm(request.POST)
                form2 = forms.SpecificRecordForm(request.POST, entry=request.POST['entry_type'])
                context = {
                    'form1':form1,
                    'project':project,
                    'form':form2,
                    }
                if form2.is_valid() and form1.is_valid():
                    # Additional form validation
                    fields = [f.name for f in models.Record._meta.get_fields()]
                    data1 = form1.clean()
                    data2 = form2.clean()

                    if data1['entry_type'] == 'book':
                        if data2['author']== '' and data2['editor'] == '':
                            context['err'] = True
                            context['errmessage'] = "Fill in either Author or Editor"
                            return render(request, 'records/record_form.html', context)
                    elif data1['entry_type'] == 'inbook':
                        if data2['author'] == '' and data2['editor'] == '':
                            context['err'] = True
                            context['errmessage'] = "Fill in either Author or Editor"
                            return render(request, 'records/record_form.html', context)
                        elif data2['chapter'] == '' and data2['pages'] == '':
                            context['err'] = True
                            context['errmessage'] = "Fill in either Chapter or Pages"
                            return render(request, 'records/record_form.html', context)
                    # Form is valid - Save.
                    record = models.Record()
                    record.entry_type = data1['entry_type']
                    record.cite_key = data1['cite_key']
                    record.project = project
                    for fieldname in fields:
                        if fieldname in data2:
                            setattr(record, fieldname, data2[fieldname])
                    record.save()
                    # Send user back to project detail, the overview of all records in the project.
                    return redirect('projects:single', slug=slug)
                else:
                    # form is not valid
                    context['err'] = True
                    return render(request, 'records/record_form.html', context)

            else:
                # User hasn't submitted yet
                context = {
                    'form1':form1,
                    'project':project,
                    }
                # Only form1 is necessary, form2 is entry specific and
                # rendered to an AJAX request.
                return render(request, 'records/record_form.html', context)
        else:
            # Access denied..
            return HttpResponse("You don't have the permission to do this")

@login_required
def keep_both_records(request, slug, pk):
    """
    This view is only available for projectmembers with editing permissions.
    This view saves handles the logic to save both of the records in case of a conflict.
    """
    # Try except to make sure the user is a member of this project
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        # User is not a member
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        # User is a member

        # Access control.. if not owner or editor - access denied.
        if pm.is_owner or pm.is_editor:
            # User has access
            project = Project.objects.get(slug=slug)
            form1 = forms.GeneralRecordForm(request.POST)
            form2 = forms.SpecificRecordForm(request.POST, entry=request.POST['entry_type'])
            context = {
                'form1':form1,
                'project':project,
                'form':form2,
                'record':models.Record.objects.get(pk=pk),
                }

            if form2.is_valid() and form1.is_valid():
                # Additional form validation
                fields = [f.name for f in models.Record._meta.get_fields()]
                data1 = form1.clean()
                data2 = form2.clean()
                if data1['entry_type'] == 'book':
                    if data2['author']== '' and data2['editor'] == '':
                        context['err'] = True
                        context['errmessage'] = "Fill in either Author or Editor"
                        return render(request, 'records/record_conflict.html', context)
                elif data1['entry_type'] == 'inbook':
                    if data2['author'] == '' and data2['editor'] == '':
                        context['err'] = True
                        context['errmessage'] = "Fill in either Author or Editor"
                        return render(request, 'records/record_conflict.html', context)
                    elif data2['chapter'] == '' and data2['pages'] == '':
                        context['err'] = True
                        context['errmessage'] = "Fill in either Chapter or Pages"
                        return render(request, 'records/record_conflict.html', context)
                # form is valid - Save.
                record = models.Record()
                record.entry_type = data1['entry_type']
                record.cite_key = data1['cite_key']
                record.project = project
                for fieldname in fields:
                    if fieldname in data2:
                        setattr(record, fieldname, data2[fieldname])
                record.save()
                # Send user back to project detail, the overview of all records in the project.
                return redirect('projects:single', slug=slug)
            else:
                # Form invalid
                context['err'] = True
                return render(request, 'records/record_conflict.html', context)
        else:
            # Access denied
            return HttpResponse("You don't have the permission to do this")
