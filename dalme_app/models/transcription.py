from django.db import models
import lxml.etree as et
from dalme_app.models._templates import dalmeUuid, get_current_username
import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)


class Transcription(dalmeUuid):
    transcription = models.TextField(blank=True, default=None)
    author = models.CharField(max_length=255, default=get_current_username)
    version = models.IntegerField(default=1)
    count_ignore = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def text_blob(self):
        xml_parser = et.XMLParser(recover=True)
        tr_tree = et.fromstring(f'<xml>{self.transcription}</xml>', xml_parser)
        return et.tostring(tr_tree, encoding='utf8', xml_declaration=False, method='text').decode('utf-8')

    @property
    def tei(self):
        return f'<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body>{self.transcription}</body></text></TEI>'
    
    @property
    def count_transcription(self):
        xml_parser = et.XMLParser(recover=True)
        tree = et.fromstring('<xml>' + self.transcription + '</xml>', xml_parser)
        tags = len(tree)

        if tags == 1 and tree[0].tag in ['quote', 'gap', 'mute'] or tags == 0:
            return not len(' '.join(t for t in tree.xpath('text()'))) == 0
        else:
            return True
