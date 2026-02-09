"""Model base page data."""

from wagtail.admin.panels import FieldPanel, FieldRowPanel, ObjectList, TabbedInterface
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.search import index
from wagtail.utils.decorators import cached_classmethod

from django.db import models

from web.extensions.extras.blocks import DEFAULT_BLOCKS
from web.extensions.footnotes.models import FootnoteMixin

HEADER_POSITION = (
    ('top', 'Top'),
    ('center', 'Center'),
    ('bottom', 'Bottom'),
)


class BasePage(Page, FootnoteMixin):
    header_image = models.ForeignKey(
        'webimages.BaseImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='The image that will display in the header.',
    )
    header_position = models.CharField(
        max_length=6,
        choices=HEADER_POSITION,
        default='top',
        help_text='The section of the image that should be centered on the header.',
    )
    short_title = models.CharField(
        max_length=63,
        null=True,
        blank=True,
        help_text='An optional short title that will be displayed in certain space constrained contexts.',
    )
    body = StreamField(DEFAULT_BLOCKS, null=True)

    search_fields = [
        *Page.search_fields,
        index.SearchField('short_title'),
        index.SearchField('body'),
    ]

    metadata_panels = [
        *Page.content_panels,
        FieldRowPanel(
            [
                FieldPanel('header_image', classname='col8'),
                FieldPanel('header_position', classname='col4'),
            ],
            heading='Header',
            classname='field-row-panel',
            icon='bandage',
        ),
    ]
    content_panels = [FieldPanel('body')]
    promote_panels = [*Page.promote_panels]

    class Meta:
        abstract = True

    def get_metadata_panels(self):
        panels = super().get_metadata_panels() if hasattr(super(), 'get_metadata_panels') else []
        if hasattr(self, 'metadata_panels'):
            panels += self.metadata_panels
        return panels

    @cached_classmethod
    def get_edit_handler(self):
        tabs = []
        if self.metadata_panels:
            tabs.append(ObjectList(self.metadata_panels, heading='Metadata'))
        if self.content_panels:
            tabs.append(ObjectList(self.content_panels, heading='Content'))
        if self.promote_panels:
            tabs.append(ObjectList(self.promote_panels, heading='Promote'))
        if self.settings_panels:
            tabs.append(ObjectList(self.settings_panels, heading='Settings'))

        edit_handler = TabbedInterface(tabs, base_form_class=self.base_form_class)
        return edit_handler.bind_to_model(self)

    def get_context(self, request):
        context = super().get_context(request)
        context.update(
            {
                'header_image': self.header_image,
                'header_position': self.header_position,
            },
        )
        return context

    @property
    def main_image(self):
        try:
            field = next(
                field
                for field in self.body
                if field.block.name == 'carousel'
                or (field.block.name == 'inline_image' and field.value.get('alignment') == 'main')
            )
        except StopIteration:
            return None
        if field.block.name == 'inline_image':
            return field.value.get('image')
        try:
            return field.value[0]
        except IndexError:
            return None

    @staticmethod
    def smart_truncate(content, length=25, suffix='...'):
        # credit: https://stackoverflow.com/questions/250357/truncate-a-string-without-ending-in-the-middle-of-a-word
        return content if len(content) <= length else ' '.join(content[: length + 1].split(' ')[0:-1]).rstrip() + suffix

    @property
    def title_switch(self):
        """Utility to reduce OR coalescing in templates.

        Prefer the short_title if a Page has one, if not fallback to title.

        """
        try:
            if self.short_title in ['Object', 'Essay', 'Inventory']:
                return self.smart_truncate(self.title)
        except AttributeError:
            return self.title
        else:
            return self.short_title or self.title
