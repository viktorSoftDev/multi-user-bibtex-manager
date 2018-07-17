from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from . import forms
from django.contrib.auth import views as auth_views
from django.forms.models import model_to_dict

# Create your views here

from django.contrib.auth import get_user_model
User = get_user_model()


class SignUp(generic.CreateView):
    form_class = forms.UserCreateForm

    success_url = reverse_lazy('login')

    template_name = 'accounts/signup.html'

def account_detail(request):
    u = request.user
    data = forms.UserCreateForm(data=model_to_dict(u))

    context = {
        'user':u,
        'data':data
    }
    template_name = 'accounts/account_detail.html'

    return render(request, template_name, context)
