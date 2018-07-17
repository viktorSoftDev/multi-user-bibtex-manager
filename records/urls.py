from django.urls import path, re_path
from . import views

app_name = 'records'

urlpatterns = [
    path('<int:pk>/', views.record_detail, name='single'),
    path('<int:pk>/edit', views.edit_record, name='edit'),
    path('<int:pk>/delete', views.delete_record, name='delete'),
    path('new/', views.create_record, name='create'),
    path('specific-form-ajax/<str:entry>/',views.specific_form_ajax, name='specific-form-ajax'),
]
