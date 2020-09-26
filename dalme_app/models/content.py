from django.db import models
from dalme_app.models._templates import dalmeIntid
import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)


class Content_attributes(dalmeIntid):
    content_type = models.ForeignKey('Content_type', to_field='id', db_index=True, on_delete=models.CASCADE, related_name='attribute_type_list')
    attribute_type = models.ForeignKey('Attribute_type', to_field='id', db_index=True, on_delete=models.CASCADE, related_name='content_types')
    order = models.IntegerField(db_index=True, null=True)
    required = models.BooleanField(default=False)
    unique = models.BooleanField(default=True)


class Content_class(dalmeIntid):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Content_type(dalmeIntid):
    content_class = models.ForeignKey('Content_class', to_field='id', db_index=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=255, unique=True)
    short_name = models.CharField(max_length=55)
    description = models.TextField()
    attribute_types = models.ManyToManyField('Attribute_type', through='Content_attributes')
    has_pages = models.BooleanField(default=False, db_index=True)
    has_inventory = models.BooleanField(default=False)
    parents = models.CharField(max_length=255, blank=True, default=None, null=True)
    r1_inheritance = models.CharField(max_length=255, blank=True, default=None, null=True)
    r2_inheritance = models.CharField(max_length=255, blank=True, default=None, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']

    @property
    def inheritance(self):
        inheritance = {}
        if self.r1_inheritance:
            inheritance['r1'] = self.r1_inheritance.split(',')
        if self.r2_inheritance:
            inheritance['r2'] = self.r2_inheritance.split(',')
        return inheritance
