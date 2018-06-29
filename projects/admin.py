from django.contrib import admin

# Register your models here.

from . import models

class ProjectMemberInline(admin.TabularInline):
    model = models.ProjectMember

class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        ProjectMemberInline,
    ]

admin.site.register(models.Project)
admin.site.register(models.ProjectMember)
