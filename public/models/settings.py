"""Model wagtail settings data."""

from wagtail import blocks
from wagtail.admin.panels import FieldPanel, FieldRowPanel, ObjectList, TabbedInterface
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.embeds.blocks import EmbedBlock
from wagtail.fields import StreamField

from django.db import models

from public.blocks import FooterPageChooserBlock, InlineImageBlock, SocialBlock
from public.models.base_page import HEADER_POSITION


@register_setting
class Settings(BaseGenericSetting):
    """Stores per-tenant settings for Wagtail."""

    name = models.CharField(
        max_length=255,
        blank=True,
        help_text='Name to be used for this site, e.g. "DALME".',
    )
    tagline = models.CharField(
        max_length=255,
        blank=True,
        help_text='Longer form tag line to be used for this site, e.g. "The Documentary Archaeology of Late Medieval Europe".',
    )
    logo = models.CharField(
        max_length=255,
        blank=True,
        help_text='Path to an image file containing a graphic logo to be used in this site, e.g. "images/dalme_logo.svg".',
    )
    copyright_line = models.CharField(
        max_length=255,
        blank=True,
        help_text='Text to add to the auto-generated copyright statement (Copyright © 20XX), e.g. "The Documentary Archaeology of Late Medieval Europe"',
    )
    footer_links = StreamField(
        [('page', FooterPageChooserBlock())],
        null=True,
        help_text='Choose pages that will appear as links in the footer.',
    )
    footer_social = StreamField(
        [('social', SocialBlock())],
        null=True,
        help_text='Choose social media apps to appear in the footer.',
    )
    search_help_content = StreamField(
        [
            ('text', blocks.RichTextBlock()),
            ('html', blocks.RawHTMLBlock()),
        ],
        null=True,
        verbose_name='Help content',
        help_text='Content to show in the search page help section.',
    )
    search_header_image = models.ForeignKey(
        'publicimages.BaseImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Header image',
        help_text='The image that will display in the header of the search page.',
    )
    search_header_position = models.CharField(
        max_length=6,
        choices=HEADER_POSITION,
        default='top',
        verbose_name='Header position',
        help_text='Position of the header image within its container.',
    )
    explore_text_before = StreamField(
        [
            ('text', blocks.RichTextBlock()),
            ('heading', blocks.CharBlock()),
            ('html', blocks.RawHTMLBlock()),
        ],
        null=True,
        verbose_name='Text before',
        help_text='Content to show before the map in the explore page.',
    )
    explore_text_after = StreamField(
        [
            ('inline_image', InlineImageBlock()),
            ('text', blocks.RichTextBlock()),
            ('heading', blocks.CharBlock()),
            ('html', blocks.RawHTMLBlock()),
            ('embed', EmbedBlock(icon='media')),
        ],
        null=True,
        verbose_name='Text after',
        help_text='Content to show after the map in the explore page.',
    )
    explore_header_image = models.ForeignKey(
        'publicimages.BaseImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Header image',
        help_text='The image that will display in the header of the explore page.',
    )
    explore_header_position = models.CharField(
        max_length=6,
        choices=HEADER_POSITION,
        default='top',
        verbose_name='Header position',
        help_text='Position of the header image within its container in the explore page.',
    )
    browser_header_image = models.ForeignKey(
        'publicimages.BaseImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Header image',
        help_text='The image that will display in the header of the record browser.',
    )
    browser_header_position = models.CharField(
        max_length=6,
        choices=HEADER_POSITION,
        default='top',
        verbose_name='Header position',
        help_text='Position of the header image within its container in the record browser.',
    )
    viewer_header_image = models.ForeignKey(
        'publicimages.BaseImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Header image',
        help_text='The image that will display in the header of the record viewer.',
    )
    viewer_header_position = models.CharField(
        max_length=6,
        choices=HEADER_POSITION,
        default='top',
        verbose_name='Header position',
        help_text='Position of the header image within its container in the record viewer.',
    )

    class Meta:
        verbose_name = 'Site preferences'

    branding_tab_panels = [
        FieldPanel('name'),
        FieldPanel('tagline'),
        FieldPanel('logo'),
    ]
    footer_tab_panel = [
        FieldPanel('copyright_line'),
        FieldPanel('footer_links'),
        FieldPanel('footer_social'),
    ]
    search_tab_panel = [
        FieldRowPanel(
            [
                FieldPanel('search_header_image', classname='col8'),
                FieldPanel('search_header_position', classname='col4'),
            ],
            heading='Header',
            classname='field-row-panel',
        ),
        FieldPanel('search_help_content'),
    ]
    explore_tab_panel = [
        FieldRowPanel(
            [
                FieldPanel('explore_header_image', classname='col8'),
                FieldPanel('explore_header_position', classname='col4'),
            ],
            heading='Header',
            classname='field-row-panel',
        ),
        FieldPanel('explore_text_before'),
        FieldPanel('explore_text_after'),
    ]
    records_tab_panel = [
        FieldRowPanel(
            [
                FieldPanel('browser_header_image', classname='col8'),
                FieldPanel('browser_header_position', classname='col4'),
            ],
            heading='Browser',
            classname='field-row-panel',
        ),
        FieldRowPanel(
            [
                FieldPanel('viewer_header_image', classname='col8'),
                FieldPanel('viewer_header_position', classname='col4'),
            ],
            heading='Viewer',
            classname='field-row-panel',
        ),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(branding_tab_panels, heading='Branding'),
            ObjectList(footer_tab_panel, heading='Footer'),
            ObjectList(search_tab_panel, heading='Search Page'),
            ObjectList(explore_tab_panel, heading='Explore Page'),
            ObjectList(records_tab_panel, heading='Record Browser/Viewer'),
        ]
    )
