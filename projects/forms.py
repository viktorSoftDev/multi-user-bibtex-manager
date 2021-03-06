
from django import forms
from . import models
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.text import slugify
from django.contrib.auth import get_user_model
User = get_user_model()

class CreateProjectForm(forms.ModelForm):
    """
    This form class handles the creation of a new project
    """
    class Meta:
        model = models.Project
        fields = ['project_title', 'description']
    # This was initially implemented to ensure users dont create projects with
    # the same slug. This has been changed in projects/models.py and is no
    # longer needed    
    # def clean(self):
    #     cleaned_data = super(CreateProjectForm, self).clean()
    #     title = cleaned_data.get('project_title')
    #     try:
    #         slug = slugify(title)
    #         models.Project.objects.get(slug=slug)
    #         raise forms.ValidationError("Sorry, that projecttitle is already in use")
    #     except ObjectDoesNotExist:
    #         pass

class ImportFileForm(forms.Form):
    """
    Simple file input form for the import file functionality
    """
    file = forms.FileInput()

class ProjectMemberForm(forms.Form):
    """
    This form allows an admin to change the project members' permissions
    """
    PERM_CHOICES = (
        ('is_owner','Admin'),
        ('is_editor','Read&Write'),
        ('is_reader','ReadOnly'),
    )
    permission = forms.ChoiceField(label="Permission", choices=PERM_CHOICES)


class InviteForm(forms.Form):
    """
    This fowm allows a project admin to invite other users
    """
    PERM_CHOICES = (
        ('is_owner','Admin'),
        ('is_editor','Read&Write'),
        ('is_reader','ReadOnly'),
    )
    email = forms.EmailField(label="Send an invitation by entering your collegue's Email")
    message = forms.CharField(label="Message", required=False)
    permission = forms.ChoiceField(label="Permission", choices=PERM_CHOICES)

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        super(InviteForm, self).__init__(*args,**kwargs)

    def clean(self):
        """
        Overwriting the clean method to add in extra validation
        """
        cleaned_data = super(InviteForm, self).clean()
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise forms.ValidationError('No user with email ' + email + ' exists' )

        try:
            models.ProjectMember.objects.get(user=User.objects.get(email=email), project=self.project)
            raise forms.ValidationError('User is already a member!')
        except ObjectDoesNotExist:
            pass

        try:
            models.Invitation.objects.get(reciever=User.objects.get(email=email), project=self.project)
            raise forms.ValidationError('User is already invited!')
        except ObjectDoesNotExist:
            pass
