from django.contrib import admin

# Register your models here.

from . import models

class ProjectMember(admin.ModelAdmin):
    fields = ['user', 'project']

    list_display = ['user', 'project']


admin.site.register(models.Project)
admin.site.register(models.ProjectMember)
