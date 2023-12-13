"""Model transcription data."""
import lxml.etree as et

from django.db import models
from django.db.models import options

from ida.models.templates import dalmeUuid, get_current_username

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Transcription(dalmeUuid):
    """Stores information about transcriptions."""

    transcription = models.TextField(blank=True)
    author = models.CharField(max_length=255, default=get_current_username)
    version = models.IntegerField(default=1)
    count_ignore = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        """Save record."""
        # Set count_ignore flag.
        xml_parser = et.XMLParser(recover=True)
        tree = et.fromstring(f'<xml>{self.transcription}</xml>', xml_parser)
        tags = len(tree)
        if tags == 1 and tree[0].tag in ['quote', 'gap', 'mute'] or tags == 0:
            self.count_ignore = len(' '.join(t for t in tree.xpath('text()'))) == 0
        super().save(*args, **kwargs)

    @property
    def text_blob(self):
        """Return text-only version of transcription."""
        xml_parser = et.XMLParser(recover=True)
        tr_tree = et.fromstring(f'<xml>{self.transcription}</xml>', xml_parser)
        return et.tostring(
            tr_tree,
            encoding='utf8',
            xml_declaration=False,
            method='text',
        ).decode('utf-8')

    @property
    def tei(self):
        """Return TEI version of transcription with proper doctype."""
        return f'<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body>{self.transcription}</body></text></TEI>'
