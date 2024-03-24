"""Form for footnote chooser."""

from django import forms


class FootnoteChooserForm(forms.Form):
    note_id = forms.CharField(widget=forms.HiddenInput())
    text = forms.CharField(widget=forms.Textarea)
