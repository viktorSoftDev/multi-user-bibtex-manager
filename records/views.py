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
# Create your views here.


from . import models
from . import forms

from django.contrib.auth import get_user_model
User = get_user_model()



def record_detail(request, slug, pk):
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






def create_record(request, slug):

    project = get_object_or_404(models.Project, slug=slug)
    context = {}
    if request.method == 'POST':
        form = forms.SaveRecordForm(request.POST)
        print(project.slug)
        if form.is_valid():
            record = form.save(commit=False)
            record.project = project
            record.save()
            return redirect('projects:single', slug=slug)
        else:
            raise ValidationError()
        
    else:
        form1 = forms.GeneralRecordForm()
        context = {
            'form1':form1,
            'project':project,
            }
    return render(request, 'records/record_form.html', context)

def specific_form_ajax(request, slug, entry):
    entry = entry
    form = forms.SpecificRecordForm(entry=entry)
    context = {'form':form}
    template = 'records/form_ajax.html'

    return render(request, template, context)
