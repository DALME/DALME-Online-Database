from django.db import models


class ContentPage(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        abstract = True


class Collection(ContentPage):
    pass


class Set(ContentPage):
    collection = models.ForeignKey(
        'dalme_public.Collection',
        related_name='sets',
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
