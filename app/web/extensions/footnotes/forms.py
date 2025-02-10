"""Form for footnote chooser."""

from django import forms

from .models import Footnote


class FootnoteForm(forms.ModelForm):
    class Meta:
        model = Footnote
        fields = ['id', 'page', 'text']
        widgets = {
            'id': forms.HiddenInput(),
            'page': forms.HiddenInput(),
        }
        labels = {'text': 'Footnote text'}
