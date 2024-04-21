"""Models for records extension."""

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, FieldRowPanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable

# from django.core.exceptions import ValidationError
from django.db import models

from ida.models import Collection, Record


class Corpus(Orderable, ClusterableModel):
    title = models.CharField(max_length=255)
    description = RichTextField()

    page = ParentalKey('public.Collections', related_name='corpora')
    collections = ParentalManyToManyField(
        'public.Collection',
        related_name='corpora',
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('collections'),
    ]

    def __str__(self):
        return self.title


def record_mixin_factory(blank=True):
    class RecordMixin(models.Model):
        record = models.ForeignKey(
            Record,
            null=True,
            blank=blank,
            on_delete=models.DO_NOTHING,
            verbose_name='Record',
            help_text='A record to associate with this page.',
        )
        record_collection = models.ForeignKey(
            Collection,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            verbose_name='Collection',
            help_text='A collection to associate with this page.',
        )

        metadata_panels = [
            FieldRowPanel(
                [
                    FieldPanel('record'),
                    FieldPanel('record_collection'),
                ],
                heading='Linked record/collection',
                classname='field-row-panel',
                icon='folder-plus',
                help_text='If both a record and a collection are selected, then the record must be a member of the collection or the page will not validate.',
            ),
        ]

        class Meta:
            abstract = True

        # def clean(self):
        #     if self.record_collection and self.record and not self.record.in_collection(self.record_collection):
        #         msg = f'Record "{self.record}" is not a member of collection "{self.record_collection}"'
        #         raise ValidationError(msg)
        #     return super().clean()

    return RecordMixin
