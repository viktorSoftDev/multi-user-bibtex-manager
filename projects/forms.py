
from django import forms
from . import models
from django.core.exceptions import ObjectDoesNotExist, ValidationError


from django.contrib.auth import get_user_model
User = get_user_model()

class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = ['project_title', 'description']


class ProjectMemberForm(forms.Form):
    PERM_CHOICES = (
        ('is_owner','Admin'),
        ('is_editor','Read&Write'),
        ('is_reader','ReadOnly'),
    )
    permission = forms.ChoiceField(label="Permission", choices=PERM_CHOICES)


class InviteForm(forms.Form):
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
