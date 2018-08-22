from material import Layout, Row, Fieldset
from django import forms
from records.models import Record
from records.data import *
from records.choices import *
from records.form_layouts import *

class GeneralRecordForm(forms.Form):
    """
    This 'general' form is simply a form with entry type and cite key, which is
    common across all records
    """

    entry_type = forms.ChoiceField(choices=ENTRY_TYPE_CHOICES, required=True)
    cite_key = forms.CharField(required=True)
    entry_type.widget.attrs.update({'class': 'form_select'})
    layout = Layout(Row('entry_type','cite_key'))

class SpecificRecordForm(forms.Form):
    """
    This form class generates a record specific form
    The data is stored in data.py
    """
    def __init__(self,*args,**kwargs):
        entry = kwargs.pop('entry')
        super().__init__(*args,**kwargs)
        for fieldname in ENTRY_TYPE_FIELDS[entry][0]:
            if fieldname == 'author':
                self.fields[fieldname] = forms.CharField(
                widget=forms.TextInput(attrs={
                    'placeholder':"          Add multiple authors separated with ' and '",
                    }))
            else:
                self.fields[fieldname] = forms.CharField()
            self.fields[fieldname].required = True

        for fieldname in ENTRY_TYPE_FIELDS[entry][1]:
            self.fields[fieldname] = forms.CharField()
            self.fields[fieldname].required = False

        self.layout = FORM_LAYOUT[entry]


class ShowRecordForm(forms.ModelForm):
    """
    This form class was created to easier be able to show the details of a record.
    """
    class Meta:
        model = Record
        fields = ['entry_type', 'cite_key']

    def __init__(self,*args,**kwargs):
        entry = kwargs.pop('entry')
        super().__init__(*args,**kwargs)
        self.fields['entry_type'].widget.attrs['readonly'] = True
        self.fields['cite_key'].widget.attrs['readonly'] = True
        self.fields['entry_type'].widget.attrs.update({'class': 'form_select'})
        for fieldname in ENTRY_TYPE_FIELDS[entry][0]:
            self.fields[fieldname] = forms.CharField()
            self.fields[fieldname].required = True
            self.fields[fieldname].widget.attrs['readonly'] = True

        for fieldname in ENTRY_TYPE_FIELDS[entry][1]:
            self.fields[fieldname] = forms.CharField()
            self.fields[fieldname].required = False
            self.fields[fieldname].widget.attrs['readonly'] = True

        self.layout = FORM_LAYOUT[entry]
