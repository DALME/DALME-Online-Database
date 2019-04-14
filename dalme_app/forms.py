"""
This is where all of the forms used elsewhere in the site are set up.
"""

from django import forms

from dalme_app.models import *

class source_main(forms.ModelForm):
    parent_source = forms.ModelChoiceField(
        queryset = Source.objects.all().order_by('name'),
        widget = forms.Select(attrs = {'class':'chosen-select'})
    )
    type = forms.ModelChoiceField(
        queryset = Content_type.objects.all().order_by('name'),
        widget = forms.Select(attrs = {'class':'chosen-select'})
    )

    class Meta:
        model = Source
        fields = ['name','short_name','type','parent_source','is_inventory']

class page_main(forms.ModelForm):
    sources = forms.ModelMultipleChoiceField(
        queryset = Source.objects.all().order_by('name'),
        widget=forms.SelectMultiple(attrs = {'class':'chosen-select'})
    )

    class Meta:
        model = Page
        fields = ['name','sources','dam_id','order']

class upload_file(forms.Form):
    inv_file = forms.FileField(label='File to upload')
