from django.db import models
from dalme_app.models._templates import dalmeUuid
import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)


class Scope(dalmeUuid):
    TEMPORAL = 1  # relationship applies only during a certain timeframe. Defined by start and end dates, start + duration, ...
    SPATIAL = 2  # relationship applies only within a certain spatial/geographical area. Defined by place id (e.g. a house, a city, a country), shapefile, polygon geometry, ...
    LINGUISTIC = 3  # relationship applies only for a language or dialect. Defined by language id.
    CONTEXT = 4  # relationship applies only in a context identified by a DALME id (e.g. a source or a page)
    SCOPE_TYPES = (
        (TEMPORAL, 'Temporal'),
        (SPATIAL, 'Spatial'),
        (LINGUISTIC, 'Linguistic'),
        (CONTEXT, 'Context')
    )

    type = models.IntegerField(choices=SCOPE_TYPES)
    range = models.TextField()  # a JSON object that contains the scope parameters, depending on its type
