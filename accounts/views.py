from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from . import forms
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()


class SignUp(generic.CreateView):
    """
    Class based view, sign up page
    """

    form_class = forms.UserCreateForm

    success_url = reverse_lazy('login')

    template_name = 'accounts/signup.html'

@login_required
def account_detail(request):
    """
    Account detail page
    """
    u = request.user
    data = forms.UserCreateForm(data=model_to_dict(u))

    context = {
        'user':u,
        'data':data
    }
    template_name = 'accounts/account_detail.html'

    return render(request, template_name, context)

@login_required
def delete_account(request):
    """
    Delete account 
    """
    u = request.user
    u.delete()

    return redirect('thanks')
