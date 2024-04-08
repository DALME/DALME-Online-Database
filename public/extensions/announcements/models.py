"""Model announcement data."""

from wagtail.fields import RichTextField
from wagtail.models import Page

from django.db import models

COLOUR_CHOICES = {
    'blue': 'Blue',
    'green': 'Green',
    'orange': 'Orange',
    'purple': 'Purple',
    'red': 'Red',
}


class Announcement(models.Model):
    id = models.AutoField(primary_key=True, unique=True, db_index=True)
    title = models.CharField(max_length=255, help_text='The title of the announcement.')
    show_title = models.BooleanField(default=True, verbose_name='Show?')
    info = RichTextField(
        features=[
            'bold',
            'italic',
            'link',
            'document-link',
            'code',
            'superscript',
            'subscript',
            'strikethrough',
            'blockquote',
            'reference',
        ],
        help_text='The main content of the announcement.',
    )
    page = models.ForeignKey(
        Page,
        on_delete=models.SET_NULL,
        related_name='announcement',
        null=True,
        help_text='If selected, a "Learn more..." button linking to a page will be included in the announcement.',
    )
    url = models.URLField(
        blank=True,
        help_text='If included a link to the URL will be added to the title of the announcement.',
    )
    color = models.CharField(max_length=10, choices=COLOUR_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return str(self.title)
