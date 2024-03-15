"""Common definitions for public models."""

from wagtail.admin.panels import FieldPanel

from ida.models import Collection

HEADER_POSITION = (
    ('top', 'Top'),
    ('center', 'Center'),
    ('bottom', 'Bottom'),
)


class SetFieldPanel(FieldPanel):
    def on_form_bound(self):
        qs = Collection.objects.filter(published=True)
        self.form.fields['source_set'].queryset = qs
        self.form.fields['source_set'].empty_label = '--------'
        super().on_form_bound()
