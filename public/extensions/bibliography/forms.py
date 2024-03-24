"""Form for reference chooser."""

from django import forms


class ReferenceLinkChooserForm(forms.Form):
    id = forms.CharField(required=True, label='Entry')
    link_text = forms.CharField(required=False)
