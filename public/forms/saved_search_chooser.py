"""Form for saved search chooser."""

from django import forms

from ida.models import SavedSearch


class SavedSearchLinkChooserForm(forms.Form):
    id = forms.ChoiceField(required=True, choices=[], label='Saved search')
    link_text = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        search_list = [(i.id, i.name) for i in SavedSearch.objects.all()]
        super().__init__(*args, **kwargs)
        self.fields['id'].choices = search_list
