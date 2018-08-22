from django.shortcuts import render
from  django.contrib.auth.decorators import login_required
from . import forms

@login_required
def specific_form_ajax(request, slug):
    """
    This function renders a specific form based on selected entry type.
    """
    form = forms.SpecificRecordForm(request.GET, entry=request.GET['entry_type'])
    context = {'form':form}
    template = 'records/form_ajax.html'
    return render(request, template, context)
