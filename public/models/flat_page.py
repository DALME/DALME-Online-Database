"""Model flat page data."""

from wagtail.admin.panels import FieldPanel

from django.contrib import messages
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import render

from public import forms
from public.models.base_page import BasePage

HEADER_POSITION = (
    ('top', 'Top'),
    ('center', 'Center'),
    ('bottom', 'Bottom'),
)


class Flat(BasePage):
    show_contact_form = models.BooleanField(
        default=False,
        help_text='Check this box to show a contact form on the page.',
    )

    citable = models.BooleanField(
        default=False,
        help_text='Check this box to show the "Cite" menu for this page.',
    )

    parent_page_types = [
        'public.Section',
        'public.Collection',
        'public.Flat',
        'public.Collections',
    ]
    subpage_types = ['public.Flat']
    page_description = 'A generic page for all kinds of content. Can be cited and show a contact form.'

    content_panels = [
        *BasePage.content_panels,
        FieldPanel('header_image'),
        FieldPanel('header_position'),
        FieldPanel('short_title'),
        FieldPanel('show_contact_form'),
        FieldPanel('citable'),
        FieldPanel('body'),
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
                'public/flat.html',
                {'page': self, 'form': form},
            )

        return super().serve(request)
