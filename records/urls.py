from django.urls import path, re_path
from . import views

app_name = 'records'

urlpatterns = [
    path('new/', views.create_record, name='create'),
    path('specific-form-ajax/<str:entry>/',views.specific_form_ajax, name='specific-form-ajax'),
]
