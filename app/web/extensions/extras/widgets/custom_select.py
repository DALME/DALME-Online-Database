"""Custom select widget."""

# workaround for: https://github.com/wagtail/wagtail/issues/11935
# see also: https://github.com/wagtail/wagtail/pull/11958

from django.forms import Select


class CustomSelect(Select):
    """Temporarily fixes an issue where select dropdowns are not selected correctly due to a missing wrapping div."""

    template_name = 'custom_select.html'
