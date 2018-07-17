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
    slug = models.SlugField(allow_unicode=True, unique=True)
    # Users could later be split up in RO_users and
    # RW_users for different permissions
    members = models.ManyToManyField(User, through="ProjectMember")

    def __str__(self):
        return self.project_title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.project_title)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('projects:single',kwargs={'slug':self.slug})

    class Meta:
        ordering = ['project_title']

class ProjectMember(models.Model):
    project = models.ForeignKey(Project, related_name='memberships', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_projects', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('project', 'user')


class Invitation(models.Model):
    project = models.ForeignKey(Project, related_name='invites', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='user_invites_sent', on_delete=models.CASCADE)
    reciever = models.ForeignKey(User, related_name='user_invites_recieved', on_delete=models.CASCADE)
    message = models.TextField(max_length=500)

    def __str__(self):
        return self.project.project_title + ' invitation from '+ self.sender.first_name + ' to ' + self.reciever.first_name
