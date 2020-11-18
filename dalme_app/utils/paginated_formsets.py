from django.utils.functional import cached_property
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.forms.formsets import ManagementForm
from django.forms import IntegerField, HiddenInput, BaseFormSet

TOTAL_FORM_COUNT = 'TOTAL_FORMS'
INITIAL_FORM_COUNT = 'INITIAL_FORMS'
MIN_NUM_FORM_COUNT = 'MIN_NUM_FORMS'
MAX_NUM_FORM_COUNT = 'MAX_NUM_FORMS'
PAGE_NUM = 'PAGE'
DEFAULT_MIN_NUM = 0
DEFAULT_MAX_NUM = 1000


class PaginatedManagementForm(ManagementForm):
    def __init__(self, *args, **kwargs):
        self.base_fields[PAGE_NUM] = IntegerField(required=False, widget=HiddenInput)
        super().__init__(*args, **kwargs)


class PaginatedBaseFormSet(BaseFormSet):
    @cached_property
    def management_form(self):
        if self.is_bound:
            form = PaginatedManagementForm(self.data, auto_id=self.auto_id, prefix=self.prefix)
            if not form.is_valid():
                raise ValidationError(
                    _('ManagementForm data is missing or has been tampered with'),
                    code='missing_management_form',
                )
        else:
            form = PaginatedManagementForm(auto_id=self.auto_id, prefix=self.prefix, initial={
                TOTAL_FORM_COUNT: self.total_form_count(),
                INITIAL_FORM_COUNT: self.initial_form_count(),
                MIN_NUM_FORM_COUNT: self.min_num,
                MAX_NUM_FORM_COUNT: self.max_num,
                PAGE_NUM: 1
            })
        return form


def formset_factory(form, formset=PaginatedBaseFormSet, extra=1, can_order=False,
                    can_delete=False, max_num=None, validate_max=False,
                    min_num=None, validate_min=False, absolute_max=None,
                    can_delete_extra=True):
    if min_num is None:
        min_num = DEFAULT_MIN_NUM
    if max_num is None:
        max_num = DEFAULT_MAX_NUM
    if absolute_max is None:
        absolute_max = max_num + DEFAULT_MAX_NUM
    if max_num > absolute_max:
        raise ValueError(
            "'absolute_max' must be greater or equal to 'max_num'."
        )
    attrs = {
        'form': form,
        'extra': extra,
        'can_order': can_order,
        'can_delete': can_delete,
        'can_delete_extra': can_delete_extra,
        'min_num': min_num,
        'max_num': max_num,
        'absolute_max': absolute_max,
        'validate_min': validate_min,
        'validate_max': validate_max,
    }
    return type(form.__name__ + 'FormSet', (formset,), attrs)
