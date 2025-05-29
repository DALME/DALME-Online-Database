"""Legacy manager for pre-8.0 MySQL database.

Enables read-only access for MySQL versions no longer supported by Django.

Inspired by: https://github.com/kloddant/django-legacy-queryset/tree/main
"""

import contextlib

import MySQLdb

from django.conf import settings
from django.core.exceptions import EmptyResultSet
from django.db import models
from django.db.models.fields.related import ForeignKey, OneToOneField, RelatedField
from django.db.models.query import EmptyQuerySet, ModelIterable, QuerySet, ValuesIterable, ValuesListIterable


class LegacyQuerySet:
    """Wrapper for QuerySet.

    Both the default manager and the base manager need to be overriden with this class.
    """

    queryset = None
    db = None
    cursor = None
    columns = []
    field_names = []
    model = None
    field_indices = []
    sql = ''
    params = ()
    iterated = False
    rows = []
    pointer = 0

    def __init__(self, queryset):
        assert isinstance(queryset, QuerySet | type(self))
        while isinstance(queryset, type(self)) and hasattr(queryset, 'queryset'):
            queryset = queryset.queryset

        self.queryset = queryset
        assert isinstance(self.queryset, QuerySet)
        self.rows = []
        self.cursor = None

        if isinstance(self.queryset, EmptyQuerySet):
            return

        compiler = self.queryset.query.get_compiler(using=self.queryset.db)
        self.columns = [x[0] for x in compiler.get_select()[0]]
        self.field_names = self.queryset._fields
        self.model = compiler.get_select()[1]['model']
        self.field_indices = compiler.get_select()[1]['select_fields']

        with contextlib.suppress(EmptyResultSet):
            self.sql, self.params = compiler.as_sql()

        self.db = MySQLdb.connect(
            host=settings.DATABASES['dam']['HOST'],
            # port=settings.DATABASES['dam']['PORT'],
            database=settings.DATABASES['dam']['NAME'],
            user=settings.DATABASES['dam']['USER'],
            password=settings.DATABASES['dam']['PASSWORD'],
        )
        self.cursor = self.db.cursor()

    def __iter__(self):
        return self.clone()

    def __next__(self, default=None):
        row = ()
        if not self.cursor and not self.iterated:
            self.cursor = self.db.cursor()
        if self.iterated:
            if self.pointer >= len(self.rows):
                self.pointer = 0
                raise StopIteration
            row = self.rows[self.pointer]
            self.pointer += 1
        elif self.cursor:
            self.execute()
            if self.cursor._executed:  # noqa: SLF001
                row = self.cursor.fetchone()
            if row:
                self.rows.append(row)
            else:
                self.close()
                raise StopIteration

        return self.row_to_object(row)

    def __getitem__(self, key):
        clone = self.clone()
        clone.fetch()
        result = list(clone)[key]
        clone.close()

        return result

    # pickle
    def __getstate__(self):
        clone = self.clone()
        state = clone.__dict__

        if 'queryset' in state:
            del state['queryset']
        if 'db' in state:
            del state['db']
        if 'cursor' in state:
            del state['cursor']

        return state

    # unpickle
    def __setstate__(self, state):
        for key, value in state.items():
            setattr(self, key, value)

        queryset = state['model'].objects.get_queryset()
        self.__init__(queryset)

    def __len__(self):
        return self.count()

    def connect(self):
        self.db = MySQLdb.connect(
            host=settings.DATABASES[self.queryset.db]['HOST'],
            # port=settings.DATABASES[self.queryset.db]['PORT'],
            database=settings.DATABASES[self.queryset.db]['NAME'],
            user=settings.DATABASES[self.queryset.db]['USER'],
            password=settings.DATABASES[self.queryset.db]['PASSWORD'],
        )
        self.cursor = self.db.cursor()

    def execute(self):
        if not self.sql:
            return
        if self.cursor._executed:  # noqa: SLF001
            return
        if self.iterated:
            return

        try:
            self.cursor.execute(self.sql, self.params)
        except:  # noqa: E722
            self.connect()
            self.execute()
            return
        self.cursor._executed = True  # noqa: SLF001

    def fetch(self):
        if not self.sql:
            return
        if not self.cursor:
            return
        if self.iterated:
            return

        _executed = self.execute()

        if self.cursor._executed:  # noqa: SLF001
            self.rows = list(self.cursor.fetchall())

        self.close()

    def clone(self):
        clone = type(self)(self.queryset)

        for key, value in self.__dict__.items():
            if key in ['db', 'cursor', 'query']:
                continue

            setattr(clone, key, value)

        return clone

    def close(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
            del self.cursor
        self.iterated = True
        self.pointer = 0

    def row_to_object(self, row):
        keys_and_values = {
            **{
                self.columns[i].target.name: row[i]
                for i in self.field_indices
                if not isinstance(self.columns[i].target, RelatedField) and i < len(row)
            },
            **{self.field_names[i]: row[i] for i in self.field_indices if self.field_names and i < len(row)},
        }
        if not hasattr(self, 'queryset') or self.queryset._iterable_class == ModelIterable:  # noqa: SLF001
            obj = self.model(**keys_and_values)
            for i in self.field_indices:
                if i >= len(self.columns) or i >= len(row):
                    break
                if isinstance(self.columns[i].target, ForeignKey | OneToOneField):
                    setattr(obj, self.columns[i].target.name + '_id', row[i])
        elif self.queryset._iterable_class == ValuesIterable:  # noqa: SLF001
            obj = keys_and_values
        elif issubclass(self.queryset._iterable_class, ValuesListIterable):  # noqa: SLF001
            obj = tuple(keys_and_values.values())
        elif settings.DEBUG:
            raise Exception(self.queryset._iterable_class)  # noqa: SLF001, TRY002
        return obj

    def first(self):
        clone = self.clone()
        result = None
        for obj in clone:
            result = obj
            break
        clone.close()
        return result

    def last(self):
        last = None
        clone = self.clone()
        for obj in clone:
            last = obj
        clone.close()
        return last

    def values(self, *fields, **expressions):
        clone = self.clone()
        values = type(self)(queryset=clone.queryset.values(*fields, **expressions))
        clone.close()
        return values

    def values_list(self, *fields, flat=False, named=False):  # noqa: ARG002
        clone = self.clone()
        if len(fields) == 1 and flat:
            values = clone.values()
            values_list = [row.get(fields[0]) for row in values]
        else:
            values_list = type(self)(queryset=clone.queryset.values_list(*fields, flat=False, named=False))
        clone.close()
        return values_list

    def count(self):
        clone = self.clone()
        clone.fetch()
        result = len(clone.rows)
        clone.close()
        return result

    def filter(self, *args, **kwargs):
        queryset = self.queryset.filter(*args, **kwargs)
        return type(self)(queryset)

    def exclude(self, *args, **kwargs):
        queryset = self.queryset.exclude(*args, **kwargs)
        return type(self)(queryset)

    def distinct(self):
        queryset = self.queryset.distinct()
        return type(self)(queryset)

    def order_by(self, *args, **kwargs):
        queryset = self.queryset.order_by(*args, **kwargs)
        return type(self)(queryset)

    def exists(self):
        return bool(self.count())

    def none(self):
        clone = self.clone()
        clone.rows = []
        clone.iterated = True
        return clone

    def all(self):
        queryset = self.queryset.all()
        return type(self)(queryset)

    def get(self, *args, **kwargs):
        queryset = self.queryset.filter(*args, **kwargs)
        return type(self)(queryset).first()

    def select_related(self, *args, **kwargs):
        queryset = self.queryset.select_related(*args, **kwargs)
        return type(self)(queryset)

    def prefetch_related(self, *args, **kwargs):
        queryset = self.queryset.prefetch_related(*args, **kwargs)
        return type(self)(queryset)

    def _add_hints(self, **hints):
        pass

    def _next_is_sticky(self):
        return self

    def using(self, alias):  # noqa: ARG002
        return self

    @property
    def ordered(self):
        return self.queryset.ordered


class LegacyManager(models.Manager):
    def get_queryset(self):
        return LegacyQuerySet(super().get_queryset())
