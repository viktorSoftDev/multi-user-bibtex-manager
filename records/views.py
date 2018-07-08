from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.http import Http404, JsonResponse
from django.contrib import messages
from braces.views import SelectRelatedMixin
from django.forms import modelform_factory, formset_factory
from django.core import serializers
from records.data import *
# Create your views here.


from . import models
from . import forms

from django.contrib.auth import get_user_model
User = get_user_model()



def record_detail(request, slug, pk):
    record = get_object_or_404(models.Record, pk=pk)
    project = models.Project.objects.get(slug=slug)
    template = 'records/record_detail.html'
    form = forms.ShowRecordForm(instance=record, entry=record.entry_type)

    data = record._meta.get_fields()

    context = {
        'record':record,
        'project':project,
        'data':data
    }

    return render(request,template,context)




class RecordList(LoginRequiredMixin,SelectRelatedMixin, generic.ListView):
    model = models.Record
    select_related = ('user', 'project')


class ProjectRecords(generic.ListView):
    model = models.Record
    template_name = 'records/project_record_list.html'

    def get_queryset(self):
        try:
            self.record_project = models.Project.objects.prefetch_related('records').get(project_title__iexact=self.kwargs.get('project_title'))
        except models.Project.DoesNotExist:
            raise Http404
        else:
            return self.record_project.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record_project'] = self.record_project
        return context



def create_record(request, slug):

    project = get_object_or_404(models.Project, slug=slug)
    context = {}
    if request.method == 'POST':
        form = forms.SaveRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.project = project
            record.save()
            return redirect('projects:single', slug=slug)
    else:
        form1 = forms.GeneralRecordForm()
        context = {
            'form1':form1,
            'project':project,
            }
    return render(request, 'records/record_form.html', context)

def specific_form_ajax(request, slug, entry):
    print(entry)
    entry = entry
    form = forms.SpecificRecordForm(entry=entry)
    context = {'form':form}
    template = 'records/form_ajax.html'

    return render(request, template, context)
