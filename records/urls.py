from django.urls import path, re_path
from . import views

app_name = 'records'

urlpatterns = [
    path('new/', views.CreateRecord.as_view(), name='create'),
]
