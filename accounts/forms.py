from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from material import Layout, Row, Fieldset
from django import forms


class MyLoginForm(AuthenticationForm):
    """
    This form class handles the authentication
    """
    def __init__(self, *args, **kwargs):
        super(MyLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'



class UserCreateForm(UserCreationForm):
    """
    This form class handles the sign up
    """

    class Meta:
        fields = ('first_name', 'last_name', 'email', 'password1','password2')
        model = get_user_model()


    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # some additional customization
        for fieldname in ['first_name', 'last_name', 'email']:
            self.fields[fieldname].required = True
        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None
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
