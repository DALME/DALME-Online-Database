from django.db import models

from solo.models import SingletonModel

from dalme_app.models import Set as DALMESet, Source


class SetAliasPage(models.Model):
    class Meta:
        abstract = True

    @property
    def description(self):
        return self.source_set.description if self.source_set else ''

    @property
    def alias_type(self):
        return self.source_set.set_type if self.source_set else None

    @property
    def sources(self):
        if self.source_set:
            return self.source_set.members.all()
        return Source.objects.none()

    def clean(self):
        if self.source_type != self.alias_type:
            mismatch = f'{self.source_type} != {self.alias_type}'
            raise ValidationError(
                f'{self._meta.label}.source_type mismatch: {mismatch}'
            )


class HomePage(SingletonModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Home"

    def __str__(self):
        return self.name


class Collection(SetAliasPage):
    set_type = DALMESet.CORPUS

    name = models.CharField(max_length=255)
    home = models.ForeignKey(
        'dalme_public.HomePage',
        related_name='collections',
        on_delete=models.CASCADE
    )
    source_set = models.ForeignKey(
        'dalme_app.Set',
        related_name='public_collections',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return self.name


class Set(SetAliasPage):
    set_type = DALMESet.COLLECTION

    name = models.CharField(max_length=255)
    collection = models.ForeignKey(
        'dalme_public.Collection',
        related_name='sets',
        on_delete=models.CASCADE
    )
    source_set = models.ForeignKey(
        'dalme_app.Set',
        related_name='public_sets',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return self.name


class MicroEssay:
    pass
