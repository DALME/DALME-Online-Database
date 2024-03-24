"""Interface for the public.forms module."""

from .contact import ContactForm
from .record_filter import RecordFilterForm

__all__ = [
    'ContactForm',
    'RecordFilterForm',
]
