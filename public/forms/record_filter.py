"""Form for records browser."""

from django import forms


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
