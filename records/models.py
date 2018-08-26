from django.db import models
from django.urls import reverse
from datetime import datetime
from django.utils import timezone
import pytz
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
    All these fields have been gathered from wikipedia
    """

    entry_type =    models.CharField(max_length=64, choices=ENTRY_TYPE_CHOICES)
    cite_key =      models.CharField(max_length=128, blank=True, default='')
    ############ All entry fields : #############

    title =         models.CharField(max_length=500, blank=True, default='')
    author =        models.CharField(max_length=500, blank=True, default='')
    journal =       models.CharField(max_length=500, blank=True, default='') # aka journaltitle
    year =          models.CharField(max_length=64, blank=True, default='')
    volume =        models.CharField(max_length=64, blank=True, default='')
    number =        models.CharField(max_length=64, blank=True, default='')
    pages =         models.CharField(max_length=64, blank=True, default='')
    month =         models.CharField(max_length=64, blank=True, default='')
    note =          models.CharField(max_length=256, blank=True, default='')

    crossref =      models.CharField(max_length=500, blank=True, default='')
    annote =        models.CharField(max_length=500, blank=True, default='')
    key =           models.CharField(max_length=500, blank=True, default='')



    editor =        models.CharField(max_length=256, blank=True, default='')
    publisher =     models.CharField(max_length=256, blank=True, default='')
    series =        models.CharField(max_length=256, blank=True, default='')
    address =       models.CharField(max_length=500, blank=True, default='')
    edition =       models.CharField(max_length=64, blank=True, default='')

    howpublished =  models.CharField(max_length=500, blank=True, default='')

    chapter =       models.CharField(max_length=64, blank=True, default='')
    type =          models.CharField(max_length=128, blank=True, default='')

    booktitle =     models.CharField(max_length=500, blank=True, default='')

    organization =  models.CharField(max_length=500, blank=True, default='')

    school =        models.CharField(max_length=256, blank=True, default='')

    institution =   models.CharField(max_length=256, blank=True, default='')

    url =           models.URLField(blank=True, default='')
    #############################################



    # A record belongs to a single project (to start with)
    project =       models.ForeignKey(Project, related_name='records', on_delete=models.CASCADE, null=True)

    # used to avoid editing conflicts
    last_edited =   models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def save(self, *args,**kwargs):
        last_edited = timezone.now()
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('projects:records:single',kwargs={'slug':self.project.slug, 'pk':self.pk})


    class Meta:
        ordering = ['-cite_key']
