
from django import forms
from . import models
from django.core.exceptions import ObjectDoesNotExist, ValidationError


from django.contrib.auth import get_user_model
User = get_user_model()

class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = ['project_title', 'description']


class InviteForm(forms.Form):
    email = forms.EmailField(label="Send an invitation by entering your collegue's Email")
    message = forms.CharField(label="Message", required=False)

    def clean(self):
        cleaned_data = super(InviteForm, self).clean()
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise forms.ValidationError('No user with email ' + email + ' exists' )
