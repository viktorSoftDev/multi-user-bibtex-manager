from material import Layout, Row, Fieldset
from django import forms
from records.models import Record
from records.data import *
from records.choices import *


class GeneralRecordForm(forms.ModelForm):

    class Meta:
        model = Record
        fields = ['entry_type']

    def update_fields(self,*args,**kwargs):
        entry_type = kwargs.pop('entry_type')

        self.fields += ENTRY_TYPES[entry_type][0] + ENTRY_TYPES[entry_type][1]

        for fieldname in ENTRY_TYPES[entry_type][0]:
            self.fields[fieldname].required = True

        for fieldname in ENTRY_TYPES[entry_type][1]:
            self.fields[fieldname].required = False
