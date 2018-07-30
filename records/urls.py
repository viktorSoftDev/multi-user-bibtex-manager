from django.urls import path, re_path
from . import views

app_name = 'records'

urlpatterns = [
    path('<int:pk>/', views.record_detail, name='single'),
    path('<int:pk>/edit', views.edit_record, name='edit'),
    path('<int:pk>/clone', views.clone_record, name='clone'),
    path('<int:pk>/delete', views.delete_record, name='delete'),
    path('<int:pk>/conflict', views.record_conflict, name='conflict'),
    path('new/', views.create_record, name='create'),
    path('specific-form-ajax/<str:entry>/',views.specific_form_ajax, name='specific-form-ajax'),
    path('keep-both-records/<int:pk>/',views.keep_both_records, name='keep_both_records'),

]
