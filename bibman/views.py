from django.shortcuts import render, get_object_or_404,redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView,
                                    ListView,
                                    DetailView,
                                    CreateView,
                                    UpdateView,
                                    DeleteView)
# Create your views here.




class ProjectsView(TemplateView):
    template_name = 'bibman/projects.html'
