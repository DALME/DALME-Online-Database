from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import options

# model imports for eval()
from dalme_app.models.reference import CountryReference, LanguageReference, LocaleReference  # noqa: F401
from dalme_app.models.rights_policy import RightsPolicy  # noqa: F401
from dalme_app.models.templates import dalmeUuid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Attribute(dalmeUuid):
    """Stores attribute data."""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.CharField(max_length=36, db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    attribute_type = models.ForeignKey(
        'AttributeType',
        db_index=True,
        on_delete=models.CASCADE,
        db_column='attribute_type',
        related_name='attributes',
    )
    # TODO: remove these fields after migration
    value_STR = models.CharField(max_length=255, blank=True)
    value_DATE_d = models.IntegerField(blank=True, null=True)
    value_DATE_m = models.IntegerField(blank=True, null=True)
    value_DATE_y = models.IntegerField(blank=True, null=True)
    value_DATE = models.DateField(blank=True, null=True)
    value_INT = models.IntegerField(blank=True, null=True)
    value_DEC = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    value_TXT = models.TextField(blank=True)
    value_JSON = models.JSONField(null=True)

    # class Meta:
    #     unique_together = ('object_id', 'attribute_type', 'value_STR')

    def __str__(self):  # noqa: D105
        return self.value_STR

    # @property
    # def value(self):
    #     """Return attribute value."""
    #     if self.attribute_type.data_type == 'DATE':
    #         return self.value_DATE if self.value_DATE is not None else self.value_STR

    #     if self.attribute_type.data_type in ['FK-UUID', 'FK-INT']:
    #         if self.value_JSON is not None:
    #             _id = self.value_JSON['id']
    #             _id = f'"{_id}"' if self.attribute_type.data_type == 'FK-UUID' else _id
    #             return eval(f"{self.value_JSON['class']}.objects.get(pk={_id})")
    #         return None

    #     return getattr(self, f'value_{self.attribute_type.data_type}')

    # @staticmethod
    # def get_date_string(day, month, year):
    #     """Return date string and date if valid."""
    #     if day is not None and month is not None and year is not None:
    #         date = f'{year!s}-{month!s}-{str(day).zfill(2)}'
    #         parsed_date = parse_date(date)
    #         ret_string = parsed_date.strftime('%d-%b-%Y').lstrip('0').replace(' 0', ' ') if parsed_date else 'Unknown'
    #         return ret_string, parsed_date

    #     if month is not None and year is not None:
    #         return f'{calendar.month_abbr[month]}-{year}', None

    #     if day is not None and month is not None:
    #         return f'{day}-{calendar.month_abbr[month]}', None

    #     if year is not None:
    #         return str(year), None

    #     return 'Unknown', None

    # def save(self, *args, **kwargs):
    #     """Save record."""
    #     data_type = self.attribute_type.data_type
    #     if data_type == 'DATE':
    #         if not self.value_DATE:
    #             date_string, date = self.get_date_string(self.value_DATE_d, self.value_DATE_m, self.value_DATE_y)
    #             if date:
    #                 self.value_DATE = date
    #         else:
    #             date_string = self.value_DATE.strftime('%d-%b-%Y').lstrip('0').replace(' 0', ' ')

    #         self.value_STR = date_string

    #     elif data_type in ['INT', 'DEC']:
    #         value = getattr(self, f'value_{data_type}', None)
    #         self.value_STR = str(value) if value is not None else ''

    #     elif data_type == 'TXT' and self.value_TXT is not None:
    #         self.value_STR = self.value_TXT[0:254] if len(self.value_TXT) > 255 else self.value_TXT

    #     elif data_type in ['FK-UUID', 'FK-INT'] and self.value_JSON is not None:
    #         _id = self.value_JSON['id']
    #         _id = f'"{_id}"' if data_type == 'FK-UUID' else _id
    #         self.value_STR = str(eval('{}.objects.get(pk={})'.format(self.value_JSON['class'], _id)))

    #     elif data_type == 'JSON' and self.value_JSON is not None:
    #         self.value_STR = 'This is a data attribute - no string representation is available.'

    #     super().save(*args, **kwargs)


class AttributeValueBool(Attribute):
    """Store for boolean attribute values."""

    value = models.BooleanField()


class AttributeValueDate(Attribute):
    """Store for date attribute values."""

    value_day = models.IntegerField(null=True)
    value_month = models.IntegerField(null=True)
    value_year = models.IntegerField(null=True)
    value_date = models.DateField(null=True)
    value_str = models.CharField(max_length=255, blank=True)


class AttributeValueDec(Attribute):
    """Store for decimal attribute values."""

    value = models.DecimalField(max_digits=9, decimal_places=2)


class AttributeValueFkey(Attribute):
    """Store for foreign key relation attribute values."""

    value = GenericForeignKey('target_content_type', 'target_id')
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='fk_attributes')
    target_id = models.CharField(max_length=36, db_index=True)


class AttributeValueInt(Attribute):
    """Store for integer attribute values."""

    value = models.IntegerField()


class AttributeValueJson(Attribute):
    """Store for JSON attribute values."""

    value = models.JSONField()


class AttributeValueStr(Attribute):
    """Store for string attribute values."""

    value = models.CharField(max_length=255)


class AttributeValueTxt(Attribute):
    """Store for text attribute values."""

    value = models.TextField()
