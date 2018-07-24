from django.urls import path, re_path, include
from . import views

app_name = 'projects'


urlpatterns = [
    path('', views.list_projects, name='all'),
    path('new/', views.CreateProject.as_view(),name='create'),
    path('<slug:slug>/records/', include('records.urls', namespace='records')),
    path('<slug:slug>/', views.SingleProject.as_view(),name='single'),
    path('<slug:slug>/leave/', views.LeaveProject.as_view(),name='leave'),
    path('<slug:slug>/invite/', views.project_invite ,name='invite'),
    path('<slug:slug>/delete/', views.DeleteProject.as_view(), name='delete'),
    path('<slug:slug>/settings/', views.project_settings, name='settings'),
    path('<slug:slug>/settings/update', views.edit_project_settings, name='edit'),
    path('<slug:slug>/accept-invite/', views.JoinProject.as_view(), name='accept'),
    path('<slug:slug>/decline-invite/', views.DeclineInvite.as_view(), name='decline'),
    path('<slug:slug>/withdraw-invite/<int:pk>', views.delete_invite, name='withdraw'),
    path('<slug:slug>/import/', views.project_import_file, name='import'),

]
