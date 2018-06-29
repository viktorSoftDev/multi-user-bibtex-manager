from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from material import Layout, Row, Fieldset
from django import forms

class UserCreateForm(UserCreationForm):


    class Meta:
        fields = ('first_name', 'last_name', 'email', 'password1','password2')
        model = get_user_model()


    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for fieldname in ['first_name', 'last_name', 'email']:
            self.fields[fieldname].required = True

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None
        # self.fields['username'].label = 'Display Name'
        self.fields['email'].error_messages = "Please provide a valid email address"

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = user.email
        if commit:
            user.save()
        return user

    layout = Layout(Row('first_name', 'last_name'),
                    'email',
                    Row('password1', 'password2'))
