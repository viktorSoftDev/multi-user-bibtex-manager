from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

#
# class UserProfile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     # Additional:
#
#     # profile picture
#
#     # personal website / linkedin  etc.
#
#     def __str__(self):
#         return self.user.username
#
# # The following 2 methods thanks to simpleisbetterthancomplex @:
# # https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.UserProfile.save()




class Project(models.Model):
    project_title = models.CharField(max_length=200)
    # Users could later be split up in RO_users and
    # RW_users for different permissions
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.project_title


class Record(models.Model):
    """
    This model contains all the fields available for
    all the various entry types. This will reduce
    repetition and simplify the relationship between
    Records and other models.
    """

    entry_type = models.CharField(max_length=64)
    cite_key = models.CharField(max_length=128, blank=True, null=True)
    ############ All entry fields : #############
    title = models.CharField(max_length=500, blank=True, null=True)
    # author =
    journal = models.CharField(max_length=500, blank=True, null=True) # aka journaltitle
    year = models.IntegerField(blank=True, null=True)
    volume = models.CharField(max_length=64, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    pages = models.CharField(max_length=64, blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, null=True)

    editor = models.CharField(max_length=256, blank=True, null=True)
    publisher = models.CharField(max_length=256, blank=True, null=True)
    series = models.CharField(max_length=256, blank=True, null=True)
    # Address could be a separate model to ensure
    # proper formatting?
    address = models.CharField(max_length=500, blank=True, null=True)
    edition = models.IntegerField(blank=True, null=True)
    isbn = models.IntegerField(blank=True, null=True) # 10 or 13 digits

    how_published = models.CharField(max_length=500, blank=True, null=True)

    chapter = models.CharField(max_length=64, blank=True, null=True)
    type = models.CharField(max_length=128, blank=True, null=True)

    booktitle = models.CharField(max_length=500, blank=True, null=True)

    organisation = models.CharField(max_length=500, blank=True, null=True)

    school = models.CharField(max_length=256, blank=True, null=True)

    institution = models.CharField(max_length=256, blank=True, null=True)

    date = models.DateField(blank=True, null=True)

    issn = models.CharField(max_length=500, blank=True, null=True)

    subtitle = models.CharField(max_length=500, blank=True, null=True)

    url = models.URLField(blank=True, null=True)
    urldate = models.DateField(blank=True, null=True)

    doi = models.CharField(max_length=500, blank=True, null=True)
    #############################################


    # A record belongs to a single project (to start with)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    # A record is made by a user, and is considered his/hers
    users = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    def destroy(self):
        """
        Checks if both project and user is null.
        If True => delete
        """

    def __str__(self):
        return self.title

class Author(models.Model):
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    # If the record is deleted, the authors belonging to
    # that records should also be deleted
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    def __str__(self):
        # This should maybe be on the form BibTeX wants it
        return self.first_name + ' ' + self.last_name

class KeyWord(models.Model):
    keyword = models.ForeignKey(Record, on_delete=models.CASCADE)

    def __str__(self):
        return self.keyword
