"""Form for records extension."""

from django import forms

from ida.models import SavedSearch


class RecordFilterForm(forms.Form):
    def clean(self):
        cleaned_data = super().clean()

        date_range = self.data.get('date_range')
        if date_range:
            try:
                after, before = date_range.split(',')
            except ValueError:
                self.add_error(
                    'date_range',
                    'Incorrect date format, should be: YYYY,YYYY',
                )

            cleaned_data['date_range'] = [after, before]

        return cleaned_data


class SavedSearchChooserForm(forms.Form):
    id = forms.ChoiceField(required=True, choices=[], label='Saved search')
    name = forms.CharField(required=True, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        search_list = [(i.id, i.name) for i in SavedSearch.objects.all()]
        super().__init__(*args, **kwargs)
        self.fields['id'].choices = search_list
