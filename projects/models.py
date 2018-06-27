from django.db import models
from django.utils.text import slugify
from django.urls import reverse


# projects MODELS.PY
# Create your models here.

from django.contrib.auth import get_user_model
User = get_user_model()

from django import template
register = template.Library()




class Project(models.Model):
    project_title = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True)
    # Users could later be split up in RO_users and
    # RW_users for different permissions
    members = models.ManyToManyField(User, through="ProjectMember")

    def __str__(self):
     return self.project_title

class ProjectMember(models.Model):
    project = models.ForeignKey(Project, related_name='memberships', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_projects', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
