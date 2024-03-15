"""Announcement banner block."""

from wagtail import blocks


class AnnouncementBannerBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    info = blocks.TextBlock()
    page = blocks.PageChooserBlock(required=False)
    url = blocks.URLBlock(required=False)
    start_date = blocks.DateBlock()
    end_date = blocks.DateBlock()

    class Meta:
        icon = 'media'
        template = 'public/blocks/_announcement_banner.html'
