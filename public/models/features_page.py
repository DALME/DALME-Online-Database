"""Model features page data."""

from wagtail.admin.panels import FieldPanel

from django.db.models.functions import Coalesce

from public.models.base_page import BasePage


class Features(BasePage):
    parent_page_types = ['public.Home']
    subpage_types = [
        'public.FeaturedObject',
        'public.FeaturedInventory',
        'public.Essay',
    ]

    content_panels = [
        *BasePage.content_panels,
        FieldPanel('header_image'),
        FieldPanel('header_position'),
        FieldPanel('short_title'),
        FieldPanel('body'),
    ]

    def get_context(self, request):
        from public.filters import FeaturedFilter

        context = super().get_context(request)
        filtered = FeaturedFilter(
            request.GET,
            queryset=self.get_children()
            .live()
            .specific()
            .annotate(
                published=Coalesce('go_live_at', 'first_published_at'),
            )
            .order_by('-published'),
        )
        context['featured'] = filtered.qs
        return context
