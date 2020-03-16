from django.db import models

from solo.models import SingletonModel


class ContentPage(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class HomePage(ContentPage, SingletonModel):
    class Meta:
        verbose_name = "Home"


class Collection(ContentPage):
    home = models.ForeignKey(
        'dalme_public.HomePage',
        related_name='collections',
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )


class Set(ContentPage):
    collection = models.ForeignKey(
        'dalme_public.Collection',
        related_name='sets',
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )


class MicroEssay:
    pass
