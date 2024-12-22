"""Model flat page data."""

from wagtail.admin.panels import FieldPanel, FieldRowPanel

from django.contrib import messages
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import render

from web import forms
from web.extensions.bibliography.models import CitableMixin
from web.models.base_page import BasePage


class Flat(BasePage, CitableMixin):
    template = 'flat.html'

    show_contact_form = models.BooleanField(
        default=False,
        help_text='Check this box to show a contact form on the page.',
    )

    parent_page_types = [
        'web.Collection',
        'web.Collections',
        'web.Flat',
        'web.Section',
    ]
    subpage_types = ['web.Flat']
    page_description = 'A generic page for all kinds of content. Can be cited and show a contact form.'

    metadata_panels = [
        *BasePage.metadata_panels,
        *CitableMixin.metadata_panels,
        FieldRowPanel(
            [
                FieldPanel('short_title', classname='col8'),
                FieldPanel('show_contact_form', classname='col4'),
            ],
            classname='field-row-panel',
        ),
    ]

    def serve(self, request):
        if self.show_contact_form:
            form = forms.ContactForm(label_suffix='')

            if request.method == 'POST':
                form = forms.ContactForm(request.POST, label_suffix='')

                if form.is_valid():
                    sent, error = form.save()
                    if sent:
                        messages.success(request, 'Your message has been delivered.')

                    else:
                        messages.error(request, f'There was a problem sending your message: {error}')

                    return HttpResponseRedirect(self.url)

            return render(
                request,
                'flat.html',
                {'page': self, 'form': form},
            )

        return super().serve(request)
