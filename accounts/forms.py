from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from material import Layout, Row, Fieldset
from django import forms

class UserCreateForm(UserCreationForm):


    class Meta:
        fields = ('first_name', 'last_name', 'username', 'email', 'password1','password2')
        model = get_user_model()


    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
        # self.fields['username'].label = 'Display Name'
        # self.fields['email'].label = "Email Address"


    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    layout = Layout(Row('first_name', 'last_name'),
                    'username', 'email',
                    Row('password1', 'password2'),
                    Fieldset('Pesonal details',
                         ))
