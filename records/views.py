from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.http import Http404, JsonResponse
from django.contrib import messages
from braces.views import SelectRelatedMixin
from django.core.exceptions import ObjectDoesNotExist
from django.forms import modelform_factory, formset_factory
from django.core import serializers
from django.forms.models import model_to_dict
from records.data import *
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
# Create your views here.

from projects.models import ProjectMember, Project
from . import models
from . import forms

from django.contrib.auth import get_user_model
User = get_user_model()


@login_required
def record_detail(request, slug, pk):
    """
    requires no extra backend access control
    """
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
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
    Only admin and readwrite should be allowed to do this
    """
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        project = get_object_or_404(models.Project, slug=slug)
        record = get_object_or_404(models.Record, pk=pk)
        pm = ProjectMember.objects.get(user=request.user, project=project)

        if pm.is_owner or pm.is_editor:
            if request.method == 'POST':
                form1 = forms.GeneralRecordForm(request.POST)
                form2 = forms.SpecificRecordForm(request.POST, entry=request.POST['entry_type'])
                if form1.is_valid() and form2.is_valid():
                    data1 = form1.clean()
                    data2 = form2.clean()
                    r.entry_type = data1['entry_type']
                    record.cite_key = data1['cite_key']
                    record.save()
                    return redirect('projects:single', slug=slug)

            else:

                form1 = forms.GeneralRecordForm(data=model_to_dict(record))
                form2 = forms.SpecificRecordForm(data=model_to_dict(record),entry=record.entry_type)
                context = {
                    'form1':form1,
                    'project':project,
                    'form2':form2,
                    'err':True
                }
                return render(request, 'records/record_copy.html', context)

            context = {
                'form1':form1,
                'form2':form2,
                'project':project,
                'record':record
            }
            return render(request, 'records/record_copy.html', context)
        else:
            return HttpResponse("You don't have the permission to do this")



@login_required
def record_conflict(request, slug, pk):
    project = Project.objects.get(slug=slug)
    if request.method == 'POST':

        if request.POST['keep'] == 'OLD':
            # old is already saved, just dont save the new one
            return redirect('projects:single', slug=slug)
        elif request.POST['keep'] == 'NEW':
            # delete old and save new!
            record = get_object_or_404(models.Record, pk=pk)
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
            record.entry_type = data1['entry_type']
            record.cite_key = data1['cite_key']
            record.project = project
            for fieldname in fields:
                if fieldname in data2:
                    setattr(record, fieldname, data2[fieldname])
            record.save()
        else:
            context['err'] = True
            return render(request, 'records/record_form.html', context)
        return redirect('projects:single', slug=slug)


@login_required
def edit_record(request, slug, pk):
    """
    Only admin and readwrite should be allowed to do this
    """
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        project = get_object_or_404(models.Project, slug=slug)
        record = get_object_or_404(models.Record, pk=pk)
        pm = ProjectMember.objects.get(user=request.user, project=project)

        if pm.is_owner or pm.is_editor:
            if request.method == 'POST':
                form1 = forms.GeneralRecordForm(request.POST)
                form2 = forms.SpecificRecordForm(request.POST, entry=request.POST['entry_type'])
                if form2.is_valid() and form1.is_valid():
                    # making sure no one has edited the record while session is running
                    print("from db: " + record.last_edited.__str__())
                    print("from session: " + request.COOKIES.get('last_edited'))
                    if record.last_edited.__str__() == request.COOKIES.get('last_edited'):
                        fields = [f.name for f in models.Record._meta.get_fields()]
                        data1 = form1.clean()
                        data2 = form2.clean()
                        record.entry_type = data1['entry_type']
                        record.cite_key = data1['cite_key']
                        record.project = project
                        for fieldname in fields:
                            if fieldname in data2:
                                setattr(record, fieldname, data2[fieldname])
                        record.save()
                        return redirect('projects:single', slug=slug)
                    else:
                        # someone changed the record before you managed to save

                        data = forms.ShowRecordForm(data=model_to_dict(record), entry=record.entry_type)
                        context = {
                            'old_record':record,
                            'form1':form1,
                            'project':project,
                            'form':form2,
                            'data':data
                        }

                        return render(request, 'records/record_conflict.html', context)

                else:
                    context = {
                        'form1':form1,
                        'project':project,
                        'form':form2,
                        'err':True
                    }
                    return render(request, 'records/record_edit.html', context)
            else:

                form1 = forms.GeneralRecordForm(data=model_to_dict(record))
                form2 = forms.SpecificRecordForm(data=model_to_dict(record),entry=record.entry_type)


            context = {
                'form1':form1,
                'form2':form2,
                'project':project,
                'record':record
            }
            response = render(request, 'records/record_edit.html', context)
            print("before: " + record.last_edited.__str__())
            response.set_cookie('last_edited', record.last_edited.__str__())
            return response
        else:
            return HttpResponse("You don't have the permission to do this")

@login_required
def delete_record(request, slug, pk):
    """
    Only admin and readwrite should be allowed to do this
    """
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        pm = ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))

        if pm.is_owner or pm.is_editor:
            record = get_object_or_404(models.Record, pk=pk)
            models.Record.objects.filter(project=get_object_or_404(models.Project, slug=slug), pk=pk).delete()
            return redirect('projects:single', slug=slug)
        else:
            return HttpResponse("You don't have the permission to do this")

@login_required
def create_record(request, slug):
    """
    Only admin and readwrite should be allowed to do this
    """
    try:
        ProjectMember.objects.get(user=request.user, project=Project.objects.get(slug=slug))
    except ObjectDoesNotExist:
        return HttpResponse("You're trying to access a project you're not a member of or a project that does not exist.")
    else:
        project = get_object_or_404(models.Project, slug=slug)
        form1 = forms.GeneralRecordForm(request.POST or None)
        pm = ProjectMember.objects.get(user=request.user, project=project)

        if pm.is_owner or pm.is_editor:
            if request.method == 'POST':
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
                    record = models.Record()
                    record.entry_type = data1['entry_type']
                    record.cite_key = data1['cite_key']
                    record.project = project
                    for fieldname in fields:
                        if fieldname in data2:
                            setattr(record, fieldname, data2[fieldname])
                    record.save()
                    print("made it")
                    return redirect('projects:single', slug=slug)
                else:
                    print("not valid")
                    context['err'] = True
                    return render(request, 'records/record_form.html', context)

            else:
                print("didnt")
                context = {
                    'form1':form1,
                    'project':project,
                    }
            return render(request, 'records/record_form.html', context)
        else:
            return HttpResponse("You don't have the permission to do this")

@login_required
def keep_both_records(request, slug, pk):
    project = Project.objects.get(slug=slug)
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
        record = models.Record()
        record.entry_type = data1['entry_type']
        record.cite_key = data1['cite_key']
        record.project = project
        for fieldname in fields:
            if fieldname in data2:
                setattr(record, fieldname, data2[fieldname])
        record.save()
    else:
        context['err'] = True
        return render(request, 'records/record_form.html', context)
    return redirect('projects:single', slug=slug)

@login_required
def specific_form_ajax(request, slug, entry):

    entry = entry

    form = forms.SpecificRecordForm(request.POST,entry=entry)
    context = {'form':form}
    template = 'records/form_ajax.html'

    return render(request, template, context)
