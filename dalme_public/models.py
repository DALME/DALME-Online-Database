from django.core.exceptions import ValidationError
from django.db import models

from solo.models import SingletonModel

from dalme_app.models import Set as DALMESet, Source


class ContentPage(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True


class SetAliasPage(models.Model):
    class Meta:
        abstract = True

    @property
    def alias_type(self):
        try:
            return self.source_set.set_type
        except AttributeError:
            return None

    @property
    def sources(self):
        if self.source_set:
            return self.source_set.members.all()
        return Source.objects.none()

    def clean(self):
        if self.alias_type is not None and self.set_type != self.alias_type:
            mismatch = f'{self.set_type} != {self.alias_type}'
            raise ValidationError(
                f'{self._meta.model.__name__}.set_type mismatch: {mismatch}'
            )


class HomePage(ContentPage, SingletonModel):
    class Meta:
        verbose_name = "Home"

    def __str__(self):
        return self.name


class Collection(ContentPage, SetAliasPage):
    set_type = DALMESet.CORPUS

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
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.name


class Set(ContentPage, SetAliasPage):
    set_type = DALMESet.COLLECTION

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
