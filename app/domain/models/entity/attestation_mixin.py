"""Mixin to connect a model instance to its attestations in the corpus."""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


class AttestationMixin(models.Model):
    attestations = GenericRelation(
        'domain.EntityPhrase',
        related_query_name='%(app_label)s_%(class)s_related',
    )

    class Meta:
        abstract = True

    @property
    def attestation_count(self):
        """Return count of attestations."""
        return self.attestations.count()

    def get_attestations_for_record(self, record):
        """Return count of attestations in a specific record."""
        tr_ids = [pn.transcription_id for pn in record.pagenodes.all()]
        return self.attestations.filter(transcription__id__in=tr_ids).count()
