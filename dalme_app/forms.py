from django import forms

class upload_inventory(forms.Form):
    inv_title = forms.CharField(label='Inventory title', help_text='A title for the inventory, normally the initials of the archive followed by series and shelf, e.g. AM FF 501.', max_length=100)
    inv_source = forms.CharField(label='Archival source', help_text='The name of the archive from where the inventory was obtained.', max_length=100)
    inv_location = forms.CharField(label='Location', help_text='The location of the archive.', max_length=100)
    inv_series = forms.CharField(label='Series', max_length=20)
    inv_shelf = forms.CharField(label='Shelf', max_length=20)
    inv_date = forms.DateField(label='Inventory date', help_text='The date in which the inventory was created.')
    inv_transcriber = forms.CharField(label='Transcriber', help_text='The author of the trascription.', max_length=100)
    inv_notes = forms.CharField(label='Notes', widget=forms.Textarea)
    inv_file = forms.FileField(label='File to upload')
