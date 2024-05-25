"""Deprecated model definitions remain here to ease migration."""

from ida.models.templates import IntIdMixin, TrackedMixin


class Source(IntIdMixin, TrackedMixin):
    pass


class Set(IntIdMixin, TrackedMixin):
    pass
