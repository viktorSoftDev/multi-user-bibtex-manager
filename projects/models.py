from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model
from django import template
User = get_user_model()
register = template.Library()




class Project(models.Model):
    project_title = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True)

    # This slug should be edited to allow for projects with the same name.
    slug = models.SlugField(allow_unicode=True, unique=True)

    # A project can have many members, and users can be members of many projects.
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
    """
    This project member class allows for further customization and access control
    """
    project = models.ForeignKey(Project, related_name='memberships', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_projects', on_delete=models.CASCADE)
    is_owner = models.BooleanField(default=False)
    is_editor = models.BooleanField(default=False)
    is_reader = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('project', 'user')


class Invitation(models.Model):
    """
    This model stores the invitation that can either be declined (deleted) or,
    if accepted, the information stored here can be used to define a new membership
    """
    project = models.ForeignKey(Project, related_name='invites', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='user_invites_sent', on_delete=models.CASCADE)
    reciever = models.ForeignKey(User, related_name='user_invites_recieved', on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
    is_owner = models.BooleanField(default=False)
    is_editor = models.BooleanField(default=False)
    is_reader = models.BooleanField(default=False)
    def __str__(self):
        return self.project.project_title + ' invitation from '+ self.sender.first_name + ' to ' + self.reciever.first_name
