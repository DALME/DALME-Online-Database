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

    def save(self, edit_mode=False):
        self.instance.save(edit_mode=edit_mode)
        self._save_m2m()
        return self.instance
