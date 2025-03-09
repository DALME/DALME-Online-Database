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
