from django.urls import path, re_path
from bibman import views

app_name = 'bibman'

urlpatterns = [
    path('', views.ProjectsView.as_view(), name='projects'),
]
