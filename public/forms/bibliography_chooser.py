"""Form for bibliography chooser."""

from django import forms


class BibliographyLinkChooserForm(forms.Form):
    id = forms.CharField(required=True, label='Entry')
    link_text = forms.CharField(required=False)
