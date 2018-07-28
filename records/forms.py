from material import Layout, Row, Fieldset
from django import forms
from records.models import Record
from records.data import *
from records.choices import *
from records.form_layouts import *

class GeneralRecordForm(forms.Form):

    entry_type = forms.ChoiceField(choices=ENTRY_TYPE_CHOICES, required=True)
    cite_key = forms.CharField(required=True)

    layout = Layout(Row('entry_type','cite_key'))

class SpecificRecordForm(forms.Form):

    def __init__(self,*args,**kwargs):
        entry = kwargs.pop('entry')
        super().__init__(*args,**kwargs)
        for fieldname in ENTRY_TYPE_FIELDS[entry][0]:
            if fieldname == 'author':
                self.fields[fieldname] = forms.CharField(widget=forms.TextInput(attrs={
                                                                                    'placeholder':"             Add multiple authors separated with ' and '",
                                                                                    }))
            else:
                self.fields[fieldname] = forms.CharField()
            self.fields[fieldname].required = True

        for fieldname in ENTRY_TYPE_FIELDS[entry][1]:
            self.fields[fieldname] = forms.CharField()
            self.fields[fieldname].required = False

        self.layout = FORM_LAYOUT[entry]


class ShowRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['entry_type', 'cite_key']

    def __init__(self,*args,**kwargs):
        entry = kwargs.pop('entry')
        super().__init__(*args,**kwargs)

        for fieldname in ENTRY_TYPE_FIELDS[entry][0]:
            self.fields[fieldname] = forms.CharField()
            self.fields[fieldname].required = True

        for fieldname in ENTRY_TYPE_FIELDS[entry][1]:
            self.fields[fieldname] = forms.CharField()
            self.fields[fieldname].required = False

        self.layout = FORM_LAYOUT[entry]
