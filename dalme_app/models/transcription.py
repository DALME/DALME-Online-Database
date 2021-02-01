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

    def save(self, **kwargs):
        # set count_ignore flag
        xml_parser = et.XMLParser(recover=True)
        tree = et.fromstring('<xml>' + self.transcription + '</xml>', xml_parser)
        tags = len(tree)

        if tags == 1 and tree[0].tag in ['quote', 'gap', 'mute'] or tags == 0:
            self.count_ignore = len(' '.join(t for t in tree.xpath('text()'))) == 0

        super(Transcription, self).save()

    @property
    def text_blob(self):
        xml_parser = et.XMLParser(recover=True)
        tr_tree = et.fromstring('<xml>' + self.transcription + '</xml>', xml_parser)
        return et.tostring(tr_tree, encoding='utf8', method='text').decode('utf-8')
