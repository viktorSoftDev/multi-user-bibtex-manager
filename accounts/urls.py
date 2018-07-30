from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import forms

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', form_class=forms.MyLoginForm),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('my-profile/', views.account_detail, name='detail'),

]
