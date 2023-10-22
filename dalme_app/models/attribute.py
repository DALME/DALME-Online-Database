from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
import json
from dalme_app.models._templates import dalmeUuid, dalmeIntid
import django.db.models.options as options
from django.utils.dateparse import parse_date
import calendar
# model imports for eval()
from dalme_app.models.reference import CountryReference, LanguageReference, LibraryReference, LocaleReference # noqa
from dalme_app.models.rights_policy import RightsPolicy # noqa

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)


class Attribute(dalmeUuid):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.UUIDField(null=True, db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    attribute_type = models.ForeignKey("Attribute_type", db_index=True, on_delete=models.CASCADE, db_column="attribute_type")
    value_STR = models.CharField(max_length=255, blank=True, null=True, default=None)
    value_DATE_d = models.IntegerField(blank=True, null=True)
    value_DATE_m = models.IntegerField(blank=True, null=True)
    value_DATE_y = models.IntegerField(blank=True, null=True)
    value_DATE = models.DateField(blank=True, null=True)
    value_INT = models.IntegerField(blank=True, null=True)
    value_DEC = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    value_TXT = models.TextField(blank=True, default=None, null=True)
    value_JSON = models.JSONField(null=True)

    class Meta:
        unique_together = ('object_id', 'attribute_type', 'value_STR')

    def __str__(self):
        return self.value_STR

    def save(self, *args, **kwargs):
        if self.attribute_type.data_type == 'DATE':
            if self.value_DATE_d is not None and self.value_DATE_m is not None and self.value_DATE_y is not None:
                date = f'{str(self.value_DATE_y)}-{str(self.value_DATE_m)}-{str(self.value_DATE_d).zfill(2)}'
                pDate = parse_date(date)
                if pDate:
                    self.value_DATE = pDate
                    self.value_STR = pDate.strftime('%d-%b-%Y').lstrip("0").replace(" 0", " ")
                else:
                    self.value_STR = 'Unknown'
            elif self.value_DATE_m is not None and self.value_DATE_y is not None:
                self.value_STR = str(calendar.month_abbr[self.value_DATE_m])+'-'+str(self.value_DATE_y)
            elif self.value_DATE_d is not None and self.value_DATE_m is not None:
                self.value_STR = str(self.value_DATE_d)+'-'+str(calendar.month_abbr[self.value_DATE_m])
            elif self.value_DATE_y is not None:
                self.value_STR = str(self.value_DATE_y)
            else:
                self.value_STR = 'Unknown'
        if self.attribute_type.data_type in ['INT', 'DEC']:
            if self.value_INT is not None:
                self.value_STR = str(self.value_INT)
            elif self.value_DEC is not None:
                self.value_STR = str(self.value_DEC)
        if self.attribute_type.data_type == 'TXT' and self.value_TXT is not None:
            self.value_STR = self.value_TXT[0:254] if len(self.value_TXT) > 255 else self.value_TXT
        if self.attribute_type.data_type in ['FK-UUID', 'FK-INT'] and self.value_JSON is not None:
            _id = '"{}"'.format(self.value_JSON['id']) if self.attribute_type.data_type == 'FK-UUID' else self.value_JSON['id']
            self.value_STR = str(eval('{}.objects.get(pk={})'.format(self.value_JSON['class'], _id)))
        super().save(*args, **kwargs)

    def get_dalme_object(self):
        if self.attribute_type.data_type == 'FK-UUID' or self.attribute_type.data_type == 'FK-INT':
            val_data = json.loads(self.value_STR)
            obj_id = '"{}"'.format(val_data['id']) if self.attribute_type.data_type == 'FK-UUID' else val_data['id']
            object = eval('{}.objects.get(pk={})'.format(val_data['class'], obj_id))
            return object


class Attribute_type(dalmeIntid):
    DATA_TYPES = (
        ('DATE', 'DATE (date)'),
        ('DEC', 'DEC (decimal)'),
        ('INT', 'INT (integer)'),
        ('STR', 'STR (string)'),
        ('TXT', 'TXT (text)'),
        ('FK-UUID', 'FK-UUID (DALME record)'),
        ('FK-INT', 'FK-INT (DALME record)')
    )

    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55, unique=True)
    description = models.TextField()
    data_type = models.CharField(max_length=15, choices=DATA_TYPES)
    source = models.CharField(max_length=255, blank=True, null=True, default=None)
    same_as = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, db_column="same_as")
    options_list = models.CharField(max_length=255, blank=True, null=True, default=None)

    def __str__(self):
        # return self.name + ' ('+self.short_name+')'
        return self.name

    class Meta:
        ordering = ['id']
