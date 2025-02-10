"""Apps module for extras extension."""

from django.apps import AppConfig
from django.db.models import ManyToManyField


class ExtraBlocksAppConfig(AppConfig):
    name = 'web.extensions.extras'
    label = 'webextras'
    verbose_name = 'IDA Extras Module'

    def ready(self):
        from wagtail.admin.forms.models import register_form_field_override

        from .widgets import MultiSelect

        register_form_field_override(ManyToManyField, override={'widget': MultiSelect})
