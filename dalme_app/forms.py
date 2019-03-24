"""
This is where all of the forms used elsewhere in the site are set up.
"""

from django import forms

from dalme_app.models import *

class source_main(forms.ModelForm):
    parent_source = forms.ModelChoiceField(
        queryset = Source.objects.all().order_by('name'),
        widget = forms.Select(attrs = {'class':'chosen-select'})
    )
    type = forms.ModelChoiceField(
        queryset = Content_type.objects.all().order_by('name'),
        widget = forms.Select(attrs = {'class':'chosen-select'})
    )

    class Meta:
        model = Source
        fields = ['name','short_name','type','parent_source','is_inventory']

class page_main(forms.ModelForm):
    sources = forms.ModelMultipleChoiceField(
        queryset = Source.objects.all().order_by('name'),
        widget=forms.SelectMultiple(attrs = {'class':'chosen-select'})
    )

    class Meta:
        model = Page
        fields = ['name','sources','dam_id','order']

class upload_file(forms.Form):
    inv_file = forms.FileField(label='File to upload')

class inventory_metadata(forms.Form):
    inv_title = forms.CharField(
        label='Inventory title',
        help_text=(
            'A title for the inventory, normally the initials of the archive '
            'followed by series and shelf, e.g. AM FF 501.'
        ),
        max_length=100
    )
    inv_source = forms.CharField(
        label='Archival source',
        help_text=(
            'The name of the archive from where the inventory was obtained.'
        ),
        max_length=100
    )
    inv_location = forms.CharField(
        label='Location',
        help_text='The location of the archive.',
        max_length=100
    )
    inv_series = forms.CharField(label='Series', max_length=20)
    inv_shelf = forms.CharField(label='Shelf', max_length=20)
    #inv_date = forms.DateField(label='Inventory date', help_text='The date in which the inventory was created.')
    inv_transcriber = forms.CharField(
        label='Transcriber',
        help_text='The author of the trascription.',
        max_length=100
    )
    #inv_notes = forms.CharField(label='Notes', widget=forms.Textarea)

class new_error(forms.Form):
    e_level = forms.IntegerField(
        label='Level',
        widget=forms.Select(choices=Notification.LEVELS)
    )
    e_type = forms.IntegerField(
        label='Type',
        widget=forms.Select(choices=Notification.TYPES)
    )
    e_text = forms.CharField(label='Text', widget=forms.Textarea)

class new_user(forms.Form):
    username = forms.CharField(label='Username', max_length=50)
    first_name = forms.CharField(label='Given name', max_length=50)
    last_name = forms.CharField(label='Surname', max_length=50)
    email = forms.CharField(label='Email', max_length=255)
    is_staff = forms.BooleanField(
        label='Staff member',
        help_text="Staff members have access to Django admin.",
        required=False
    )
    is_superuser = forms.BooleanField(label='Superuser', required=False)
    dam_usergroup = forms.IntegerField(
        label='DAM user group',
        widget=forms.Select(choices=Profile.DAM_USERGROUPS)
    )
    wiki_groups = forms.MultipleChoiceField(
        label='Wiki groups',
        help_text="Use CMD to choose multiple groups.",
        choices=Profile.WIKI_GROUPS
    )
    wp_role = forms.CharField(
        label='WP role',
        widget=forms.Select(choices=Profile.WP_ROLE)
    )

#class home_search(forms.Form):
#    search_string = forms.CharField()
