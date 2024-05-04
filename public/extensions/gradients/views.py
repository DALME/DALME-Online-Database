"""Views for gradients."""

from wagtail.admin.admin_url_finder import AdminURLFinder
from wagtail.admin.panels import FieldPanel, FieldRowPanel
from wagtail.admin.ui.tables import Column, TitleColumn, UpdatedAtColumn
from wagtail.admin.views.generic.chooser import (
    ChooseView,
    ChosenResponseMixin,
    ChosenViewMixin,
)
from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.admin.viewsets.model import ModelViewSet
from wagtail.admin.widgets import BaseChooser

from django import forms
from django.contrib.admin.utils import quote
from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic.base import View

from public.extensions.extras.widgets import ColourPickerWidget

from .models import Gradient


class GradientChooseView(ChooseView):
    @property
    def columns(self):
        return [
            TitleColumn(
                'gradient_as_html',
                label='Gradient',
                get_url=(
                    lambda obj: self.append_preserved_url_parameters(
                        reverse(self.chosen_url_name, args=(quote(obj.pk),))
                    )
                ),
                link_attrs={'data-chooser-modal-choice': True},
            ),
            Column('description', label='Description'),
        ]


class GradientChosenResponseMixin(ChosenResponseMixin):
    def get_chosen_response_data(self, item):
        response_data = super().get_chosen_response_data(item)
        response_data.update(
            {
                'gradient': item.gradient_as_html(),
                'description': item.description,
            }
        )
        return response_data


class GradientChosenView(ChosenViewMixin, GradientChosenResponseMixin, View):
    pass


class AdminGradientChooser(BaseChooser):
    model = Gradient
    chooser_modal_url_name = 'gradient_chooser:choose'
    template_name = 'gradient_chooser.html'
    js_constructor = 'GradientChooser'

    def get_value_data_from_instance(self, instance):
        return {
            'id': instance.pk,
            'edit_url': AdminURLFinder().get_edit_url(instance),
            self.display_title_key: self.get_display_title(instance),
            'gradient': instance.gradient_as_html(),
            'description': instance.description,
        }

    def get_context(self, name, value_data, attrs):
        original_field_html = self.render_hidden_input(name, value_data.get('id'), attrs)
        return {
            'widget': self,
            'original_field_html': original_field_html,
            'attrs': attrs,
            'value': bool(value_data),
            'edit_url': value_data.get('edit_url', ''),
            'display_title': value_data.get(self.display_title_key, ''),
            'gradient': value_data.get('gradient'),
            'description': value_data.get('description'),
            'chooser_url': self.get_chooser_modal_url(),
            'icon': self.icon,
            'classname': self.classname,
        }

    @cached_property
    def media(self):
        base_media = super().media
        return forms.Media(
            js=[
                *base_media._js,  # noqa: SLF001
                'wagtailadmin/js/chooser-modal.js',
                'js/gradient-chooser-modal.js',
            ]
        )


class GradientChooserViewSet(ChooserViewSet):
    model = Gradient
    name = 'gradient_chooser'
    icon = 'swatchbook'
    choose_one_text = 'Choose a gradient'
    base_widget_class = AdminGradientChooser
    choose_view_class = GradientChooseView
    chosen_view_class = GradientChosenView


class GradientViewSet(ModelViewSet):
    model = Gradient
    add_to_reference_index = False
    icon = 'swatchbook'
    menu_label = 'Gradients'
    menu_name = 'gradients'
    menu_order = 900
    add_to_settings_menu = True
    list_display = ['gradient_as_html', 'description', UpdatedAtColumn()]
    columns = ['Gradient', 'Description', 'Updated']
    chooser_viewset_class = GradientChooserViewSet
    list_filter = ['description']
    search_fields = ['description']
    search_backend_name = False

    panels = [
        FieldRowPanel(
            [
                FieldPanel('colour_1', widget=ColourPickerWidget()),
                FieldPanel('colour_2', widget=ColourPickerWidget()),
                FieldPanel('angle'),
            ],
            heading='Gradient Attributes',
            classname='field-row-panel',
        ),
        FieldPanel('description'),
    ]
