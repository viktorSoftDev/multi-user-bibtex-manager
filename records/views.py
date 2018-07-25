from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.http import Http404, JsonResponse
from django.contrib import messages
from braces.views import SelectRelatedMixin
from django.forms import modelform_factory, formset_factory
from django.core import serializers
from django.forms.models import model_to_dict
from records.data import *
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
# Create your views here.


from . import models
from . import forms

from django.contrib.auth import get_user_model
User = get_user_model()


@login_required
def record_detail(request, slug, pk):
    """
    requires no extra backend access control
    """
    record = get_object_or_404(models.Record, pk=pk)
    project = models.Project.objects.get(slug=slug)
    template = 'records/record_detail.html'
    data = forms.ShowRecordForm(data=model_to_dict(record), entry=record.entry_type)

    context = {
        'record':record,
        'project':project,
        'data':data
    }

    return render(request,template,context)

@login_required
def clone_record(request, slug, pk):
    """
    Only admin and readwrite should be allowed to do this
    """
    project = get_object_or_404(models.Project, slug=slug)
    record = get_object_or_404(models.Record, pk=pk)

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

@login_required
def edit_record(request, slug, pk):
    """
    Only admin and readwrite should be allowed to do this
    """
    project = get_object_or_404(models.Project, slug=slug)
    record = get_object_or_404(models.Record, pk=pk)
    if request.method == 'POST':
        form1 = forms.GeneralRecordForm(request.POST)
        form2 = forms.SpecificRecordForm(request.POST, entry=request.POST['entry_type'])
        if form2.is_valid() and form1.is_valid():
            fields = [f.name for f in models.Record._meta.get_fields()]
            data1 = form1.clean()
            data2 = form2.clean()
            record = models.Record()
            record.entry_type = data1['entry_type']
            record.cite_key = data1['cite_key']
            record.project = project
            for fieldname in fields:
                if fieldname in data2:
                    setattr(record, fieldname, data2[fieldname])
            record.save()
            return redirect('projects:single', slug=slug)
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
    return render(request, 'records/record_edit.html', context)

@login_required
def delete_record(request, slug, pk):
    """
    Only admin and readwrite should be allowed to do this
    """
    record = get_object_or_404(models.Record, pk=pk)
    models.Record.objects.filter(project=get_object_or_404(models.Project, slug=slug), pk=pk).delete()
    return redirect('projects:single', slug=slug)

@login_required
def create_record(request, slug):
    """
    Only admin and readwrite should be allowed to do this
    """
    project = get_object_or_404(models.Project, slug=slug)
    form1 = forms.GeneralRecordForm(request.POST or None)

    if request.method == 'POST':
        form1 = forms.GeneralRecordForm(request.POST)
        form2 = forms.SpecificRecordForm(request.POST, entry=request.POST['entry_type'])
        if form2.is_valid() and form1.is_valid():
            fields = [f.name for f in models.Record._meta.get_fields()]
            data1 = form1.clean()
            data2 = form2.clean()
            record = models.Record()
            record.entry_type = data1['entry_type']
            record.cite_key = data1['cite_key']
            record.project = project
            for fieldname in fields:
                if fieldname in data2:
                    setattr(record, fieldname, data2[fieldname])
            record.save()
            return redirect('projects:single', slug=slug)
        else:
            context = {
                'form1':form1,
                'project':project,
                'form':form2,
                'err':True
            }
            return render(request, 'records/record_form.html', context)

    else:

        context = {
            'form1':form1,
            'project':project,
            }
    return render(request, 'records/record_form.html', context)

@login_required
def specific_form_ajax(request, slug, entry):
    """
    Only admin and readwrite should be allowed to do this
    """
    entry = entry

    form = forms.SpecificRecordForm(request.POST,entry=entry)
    context = {'form':form}
    template = 'records/form_ajax.html'

    return render(request, template, context)
