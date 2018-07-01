from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.http import Http404
from django.contrib import messages
from braces.views import SelectRelatedMixin
# Create your views here.


from . import models
from . import forms

from django.contrib.auth import get_user_model
User = get_user_model()


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



class CreateRecord(LoginRequiredMixin,generic.CreateView):
    model = models.Record
    fields = ['entry_type']
