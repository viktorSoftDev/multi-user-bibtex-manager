from material import Layout, Row, Fieldset
from django import forms
from records.models import Record
from records.data import *
from records.choices import *
from records.form_layouts import *

class GeneralRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ["entry_type", "cite_key"]

class SpecificRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        exclude = ['entry_type', 'cite_key']

    def __init__(self,*args,**kwargs):
        entry = kwargs.pop('entry')
        super().__init__(*args,**kwargs)
        for fieldname in ENTRY_TYPE_FIELDS[entry][0]:
            self.fields[fieldname] = forms.CharField(required=True)

        for fieldname in ENTRY_TYPE_FIELDS[entry][1]:
            self.fields[fieldname] = forms.CharField(required=False)

        self.layout = FORM_LAYOUT[entry]

class SaveRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = '__all__'

class ShowRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['entry_type', 'cite_key']

    def __init__(self,*args,**kwargs):
        entry = kwargs.pop('entry')
        super().__init__(*args,**kwargs)
        for fieldname in ENTRY_TYPE_FIELDS[entry][0]:
            self.fields[fieldname] = forms.CharField(required=True)

        for fieldname in ENTRY_TYPE_FIELDS[entry][1]:
            self.fields[fieldname] = forms.CharField(required=False)

        self.layout = FORM_LAYOUT[entry]
