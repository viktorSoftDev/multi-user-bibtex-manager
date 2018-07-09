from django.db import models
from django.urls import reverse
from django.conf import Settings
from datetime import datetime
from django.utils.text import slugify

# POST MODELS.PY
# Create your models here.

from projects.models import Project
from records.choices import *

from django.contrib.auth import get_user_model
User = get_user_model()


class Record(models.Model):
    """
    This model contains all the fields available for
    all the various entry types. This will reduce
    repetition and simplify the relationship between
    Records and other models.
    """

    entry_type =    models.CharField(max_length=64, choices=ENTRY_TYPE_CHOICES)
    cite_key =      models.CharField(max_length=128, null=True)
    ############ All entry fields : #############

    title =         models.CharField(max_length=500, null=True)
    author =        models.CharField(max_length=500, null=True)
    journal =       models.CharField(max_length=500,null=True) # aka journaltitle
    year =          models.IntegerField(null=True)
    volume =        models.CharField(max_length=64, null=True)
    number =        models.IntegerField(null=True)
    pages =         models.CharField(max_length=64, null=True)
    month =         models.IntegerField(null=True)
    note =          models.CharField(max_length=256, null=True)

    editor =        models.CharField(max_length=256, null=True)
    publisher =     models.CharField(max_length=256, null=True)
    series =        models.CharField(max_length=256, null=True)
    address =       models.CharField(max_length=500, null=True)
    edition =       models.IntegerField(null=True)
    isbn =          models.IntegerField(null=True) # 10 or 13 digits

    how_published = models.CharField(max_length=500, null=True)

    chapter =       models.CharField(max_length=64, null=True)
    type =          models.CharField(max_length=128, null=True)

    booktitle =     models.CharField(max_length=500, null=True)

    organisation =  models.CharField(max_length=500, null=True)

    school =        models.CharField(max_length=256, null=True)

    institution =   models.CharField(max_length=256, null=True)

    date =          models.DateField(null=True)

    issn =          models.CharField(max_length=500, null=True)

    subtitle =      models.CharField(max_length=500, null=True)

    url =           models.URLField(null=True)
    urldate =       models.DateField(null=True)

    doi =           models.CharField(max_length=500, null=True)
    #############################################



    # A record belongs to a single project (to start with)
    project =       models.ForeignKey(Project, related_name='records', on_delete=models.SET_NULL, null=True)
    # A record is made by a user, and is considered his/hers
    # users = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    last_edited =   models.DateTimeField(default=datetime.now)

    # def destroy(self):
    #     """
    #     Checks if both project and user is null.
    #     If True => delete
    #     """
    #     if self.project == null and self.users == null:
    #         self.delete()

    def __str__(self):
        return self.title

    def save(self, *args,**kwargs):
        last_edited = datetime.now()

        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('projects:records:single',kwargs={'slug':self.project.slug, 'pk':self.pk})


    class Meta:
        ordering = ['-cite_key']
