from material import Layout, Row, Fieldset
from django import forms
from records.models import Record
from records.data import *
from records.choices import *


class GeneralRecordForm(forms.ModelForm):

    class Meta:
        model = Record

    def __init__(self, *args, **kwargs):
        entry_type = kwargs.pop('entry_type')
        super(GeneralRecordForm, self).__init__(*args, **kwargs)

        """
        fields =  ENTRY_TYPES("entry_type")[0] + ENTRY_TYPES("entry_type")[1]
        """


        for fieldname in ENTRY_TYPES("entry_type"):
            pass
