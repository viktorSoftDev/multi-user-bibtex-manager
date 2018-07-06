from django.urls import path, re_path, include
from . import views

app_name = 'projects'


urlpatterns = [
    path('', views.ListProjects.as_view(), name='all'),
    path('new/', views.CreateProject.as_view(),name='create'),
    path('<slug:slug>/records/', include('records.urls', namespace='records')),
    path('<slug:slug>/', views.SingleProject.as_view(),name='single'),
    path('leave/<slug:slug>/', views.LeaveProject.as_view(),name='leave'),
    # join
    # invite
]
