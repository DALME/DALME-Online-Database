"""Apps module for announcements extension."""

from django.apps import AppConfig


class AnnouncementsAppConfig(AppConfig):
    name = 'public.extensions.announcements'
    label = 'publicannouncements'
    verbose_name = 'IDA Announcements Module'
