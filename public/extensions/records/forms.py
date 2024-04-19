"""Form for records extension."""

from django import forms

from ida.models import SavedSearch


class SavedSearchChooserForm(forms.Form):
    id = forms.ChoiceField(required=True, choices=[], label='Saved search')
    name = forms.CharField(required=True, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        search_list = [(i.id, i.name) for i in SavedSearch.objects.all()]
        super().__init__(*args, **kwargs)
        self.fields['id'].choices = search_list
