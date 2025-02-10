"""Form for reference chooser."""

from django import forms


class ReferenceChooserForm(forms.Form):
    id = forms.CharField(required=True, label='Reference', widget=forms.Select())
    biblio = forms.ChoiceField(required=True, label='Show in')
    reference = forms.CharField(required=True, widget=forms.HiddenInput())
