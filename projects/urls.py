from django.urls import path, re_path
from . import views

app_name = 'projects'


urlpatterns = [
    path('', views.ListProjects.as_view(), name='all'),
    path('new/', views.CreateProject.as_view(),'create'),
    re_path(r'^records/in/(?P<slug>[-\w]+)/$', views.SingleProject.as_view(),name='single'),
    re_path(r'^leave/(?P<slug>[-\w]+)/$', views.LeaveProject.as_view(),name='leave'),
    # join
    # invite
]
