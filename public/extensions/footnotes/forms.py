"""Form for footnote chooser."""

from wagtail.admin.forms.models import WagtailAdminModelForm

from django.forms import HiddenInput

from .models import Footnote


class FootnoteChooserForm(WagtailAdminModelForm):
    class Meta:
        model = Footnote
        fields = ['id', 'page', 'text']
        widgets = {
            'id': HiddenInput(),
            'page': HiddenInput(),
        }
        labels = {'text': 'Footnote text'}
