"""Attribute-related models."""

import calendar
import datetime

from dateutil.parser import parse

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import options

from .templates import TrackedMixin, UuidMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Attribute(UuidMixin, TrackedMixin):
    """Stores attribute data."""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.CharField(max_length=36, db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    attribute_type = models.ForeignKey(
        'ida.AttributeType',
        db_index=True,
        on_delete=models.CASCADE,
        related_name='attributes',
    )

    def __str__(self):
        return f'{self.attribute_type.name}: {self.value}'

    @property
    def name(self):
        """Return attribute name."""
        return self.attribute_type.name

    @property
    def label(self):
        """Return attribute label."""
        return self.attribute_type.label

    @property
    def description(self):
        """Return attribute description."""
        return self.attribute_type.description

    @property
    def data_type(self):
        """Return attribute data type."""
        return self.attribute_type.data_type

    @property
    def value(self):
        """Return attribute value."""
        if self.attribute_type.data_type == 'RREL':
            return None
        store = getattr(self, f'attributevalue{self.attribute_type.data_type.lower()}')
        return store.value

    def get_options(self):
        """Return options for attribute."""
        qs = self.attribute_type.content_types.filter(content_type=self.content_type.extended.id)
        if qs.exists():
            override_options = qs.first().override_options
        else:
            qs = self.attribute_type.content_types.filter(content_type=self.content_object.type.id)
            override_options = qs.first().override_options if qs.exists() else None
        return override_options if override_options else self.attribute_type.options


class AttributeValueBool(Attribute):
    """Store for boolean attribute values."""

    value = models.BooleanField()

    def __str__(self):
        return str(self.value)


class AttributeValueDate(Attribute):
    """Store for date attribute values."""

    day = models.PositiveSmallIntegerField(
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(31)],
    )
    month = models.PositiveSmallIntegerField(
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
    )
    year = models.IntegerField(null=True)
    date = models.DateField(null=True)
    text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.text

    @property
    def value(self):
        """Return value of date."""
        return {
            'day': self.day,
            'month': self.month,
            'year': self.year,
            'date': self.date,
            'text': self.text,
        }

    def save(self, *args, **kwargs):  # noqa: C901, PLR0912
        """Override save method to format date."""
        if self.date:
            try:
                date = parse(self.date)
            except TypeError:
                date = self.date
            self.day = date.day
            self.month = date.month
            self.year = date.year
            self.text = self.get_date_string(date=date)

        elif self.day and self.month and self.year:
            date = None
            try:
                date = datetime.date(self.year, self.month, self.day)
            except ValueError:
                date = parse(
                    f'{self.year!s}-{str(self.month).zfill(2)}-{str(self.day).zfill(2)}',
                )
            if date is not None:
                self.date = date
                self.text = self.get_date_string(date=date)
            else:
                self.text = self.get_date_string(
                    day=self.day,
                    month=self.month,
                    year=self.year,
                )

        elif self.day or self.month or self.year:
            if not self.text:
                self.text = self.get_date_string(
                    day=self.day,
                    month=self.month,
                    year=self.year,
                )

        elif self.text:
            try:
                date = parse(self.text)
            except ValueError:
                date = None

            if date is not None:
                self.date = date
                self.day = date.day
                self.month = date.month
                self.year = date.year
                self.text = self.get_date_string(date=date)

        super().save(*args, **kwargs)

    @staticmethod
    def get_date_string(date=None, day=None, month=None, year=None):
        """Return date string."""
        if date is not None:
            return date.strftime('%d-%b-%Y').lstrip('0').replace(' 0', ' ')

        if month is not None and year is not None:
            return f'{calendar.month_abbr[month]} {year}'

        if day is not None and month is not None:
            return f'{day} {calendar.month_abbr[month]}'

        if year is not None:
            return str(year)

        return 'Unknown date'


class AttributeValueDec(Attribute):
    """Store for decimal attribute values."""

    value = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.value)


class AttributeValueFkey(Attribute):
    """Store for foreign key relation attribute values."""

    value = GenericForeignKey('target_content_type', 'target_id')
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='fk_attributes',
    )
    target_id = models.CharField(max_length=36, db_index=True)

    def __str__(self):
        return str(self.value)


class AttributeValueInt(Attribute):
    """Store for integer attribute values."""

    value = models.IntegerField()

    def __str__(self):
        return str(self.value)


class AttributeValueJson(Attribute):
    """Store for JSON attribute values."""

    value = models.JSONField()

    def __str__(self):
        return '<DATA OBJECT>'


class AttributeValueStr(Attribute):
    """Store for string attribute values."""

    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value


class AttributeValueTxt(Attribute):
    """Store for text attribute values."""

    value = models.TextField()

    def __str__(self):
        return self.value
