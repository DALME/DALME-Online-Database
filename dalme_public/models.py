from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Count, F, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from modelcluster.fields import ParentalKey

from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core import blocks, hooks
from wagtail.core.models import Orderable, Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtailmodelchooser import register_model_chooser, Chooser
from wagtailmodelchooser.edit_handlers import ModelChooserPanel

from dalme_app.models import Set as DALMESet, Source
from dalme_app.serializers import SourceSerializer


# https://github.com/django/django/blob/master/django/urls/converters.py#L26
UUID_RE = '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'


@hooks.register('before_serve_page')
def redirect_root(page, request, serve_args, serve_kwargs):
    if page.is_root():
        home = page.get_children().first()
        return redirect(home.url, permanent=False)


@register_model_chooser
class SourceChooser(Chooser):
    model = Source

    def get_queryset(self, request):
        qs = super().get_queryset(request).order_by('name')
        if request.GET.get('q'):
            # TODO: OR this with an ID filter
            qs = qs.filter(name__icontains=request.GET['q'])
        return qs


class DALMEImage(AbstractImage):
    caption = models.CharField(max_length=255, null=True, blank=True)

    admin_form_fields = Image.admin_form_fields + ('caption',)


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        DALMEImage, on_delete=models.CASCADE, related_name='renditions'
    )

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )


class CarouselMixin(Orderable):
    carousel_image = models.ForeignKey(
        'dalme_public.DALMEImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [ImageChooserPanel('carousel_image')]


class SubsectionBlock(blocks.StructBlock):
    heading = blocks.CharBlock()
    body = blocks.RichTextBlock()

    class Meta:
        icon = 'arrow-right'


class DALMEPage(Page):
    header_image = models.ForeignKey(
        'dalme_public.DALMEImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = RichTextField()
    short_title = models.CharField(
        max_length=63,
        null=True,
        blank=True,
        help_text='An optional short title that will be displayed in certain contexts.'
    )

    class Meta:
        abstract = True

    @property
    def title_switch(self):
        """Utility to reduce OR coalescing in templates.
        Prefer the short_title if a Page has one, if not fallback to title.
        """
        try:
            return self.short_title or self.title
        except AttributeError:
            return self.title


class Home(DALMEPage):
    subpage_types = [
        'dalme_public.Flat',
        'dalme_public.Features',
        'dalme_public.Collections'
    ]

    content_panels = DALMEPage.content_panels + [
        ImageChooserPanel('header_image'),
        FieldPanel('body', classname='full'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['featured_object'] = FeaturedObject.objects.live().first()
        context['featured_inventory'] = FeaturedInventory.objects.live().first()
        context['essay'] = Essay.objects.live().first()
        return context


class Flat(DALMEPage):
    main_image = models.ForeignKey(
        'dalme_public.DALMEImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    inline_image = models.ForeignKey(
        'dalme_public.DALMEImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    parent_page_types = ['dalme_public.Home']
    subpage_types = ['dalme_public.Flat']

    content_panels = DALMEPage.content_panels + [
        ImageChooserPanel('header_image'),
        ImageChooserPanel('main_image'),
        ImageChooserPanel('inline_image'),
        FieldPanel('short_title'),
        FieldPanel('body', classname='full'),
    ]


class Features(DALMEPage):
    parent_page_types = ['dalme_public.Home']
    subpage_types = [
        'dalme_public.FeaturedObject',
        'dalme_public.FeaturedInventory',
        'dalme_public.Essay'
    ]

    content_panels = DALMEPage.content_panels + [
        ImageChooserPanel('header_image'),
        FieldPanel('short_title'),
        FieldPanel('body', classname='full'),
    ]


class FeaturedMixin:
    @property
    def author(self):
        return f'{self.owner.first_name} {self.owner.last_name}'


class FeaturedObjectCarousel(CarouselMixin):
    page = ParentalKey(
        'dalme_public.FeaturedObject', related_name='carousel'
    )


class FeaturedObject(FeaturedMixin, DALMEPage):
    short_title = 'Object'
    phrase = RichTextField(null=True, blank=True)
    source = models.ForeignKey(
        'dalme_app.Source',
        related_name='featured_objects',
        on_delete=models.PROTECT
    )

    parent_page_types = ['dalme_public.Features']
    subpage_types = []

    content_panels = DALMEPage.content_panels + [
        ImageChooserPanel('header_image'),
        ModelChooserPanel('source'),
        FieldPanel('phrase', classname='full'),
        FieldPanel('body', classname='full'),
        MultiFieldPanel(
            [InlinePanel('carousel', min_num=1, label='Image')],
            heading='Carousel Images',
        )
    ]

    @property
    def main_image(self):
        try:
            return self.carousel.first().carousel_image
        except AttributeError:
            return None


class FeaturedInventory(FeaturedMixin, DALMEPage):
    short_title = 'Inventory'
    source = models.ForeignKey(
        'dalme_app.Source',
        related_name='featured_inventories',
        on_delete=models.PROTECT
    )
    alt_image = models.ForeignKey(
        'dalme_public.DALMEImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='An alternate image taking priority over any on the Source.'
    )

    parent_page_types = ['dalme_public.Features']
    subpage_types = []

    content_panels = DALMEPage.content_panels + [
        ImageChooserPanel('header_image'),
        ModelChooserPanel('source'),
        ImageChooserPanel('alt_image'),
        FieldPanel('body', classname='full'),
    ]


class Essay(FeaturedMixin, DALMEPage):
    short_title = 'Essay'
    source = models.ForeignKey(
        'dalme_app.Source',
        related_name='essays',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    alt_image = models.ForeignKey(
        'dalme_public.DALMEImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='An alternate image taking priority over any on the Source.'
    )

    parent_page_types = ['dalme_public.Features']
    subpage_types = []

    content_panels = DALMEPage.content_panels + [
        ImageChooserPanel('header_image'),
        FieldPanel('source', classname='full'),
        ImageChooserPanel('alt_image'),
        FieldPanel('body', classname='full'),
    ]


class Collections(DALMEPage):
    parent_page_types = ['dalme_public.Home']
    subpage_types = ['dalme_public.Collection']

    content_panels = DALMEPage.content_panels + [
        ImageChooserPanel('header_image'),
        FieldPanel('short_title'),
        FieldPanel('body', classname='full'),
    ]


class Collection(DALMEPage):
    description = RichTextField()

    parent_page_types = ['dalme_public.Collections']
    subpage_types = ['dalme_public.Set']

    content_panels = DALMEPage.content_panels + [
        ImageChooserPanel('header_image'),
        FieldPanel('description', classname='full'),
        FieldPanel('body', classname='full'),
    ]


class Set(RoutablePageMixin, DALMEPage):
    set_type = DALMESet.COLLECTION
    source_set = models.ForeignKey(
        'dalme_app.Set',
        related_name='public_sets',
        on_delete=models.PROTECT
    )

    main_image = models.ForeignKey(
        'dalme_public.DALMEImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    description = RichTextField()
    subsections = StreamField([
        ('subsection', SubsectionBlock())
    ])

    parent_page_types = ['dalme_public.Collection']
    subpage_types = []

    content_panels = DALMEPage.content_panels + [
        FieldPanel('source_set', classname='full'),
        ImageChooserPanel('header_image'),
        ImageChooserPanel('main_image'),
        FieldPanel('description', classname='full'),
        FieldPanel('body', classname='full'),
        StreamFieldPanel('subsections'),
    ]

    @route(r'^inventories/$', name='inventories')
    def inventories(self, request):
        context = self.get_context(request)
        context.update({
            'inventories': True,
            'set_id': self.source_set.id,
        })
        return TemplateResponse(
          request, 'dalme_public/inventories.html', context
        )

    @route(rf'^inventories/({UUID_RE})/$', name='inventory')
    def inventory(self, request, pk):
        qs = Source.objects.filter(pk=pk)
        if not qs.exists():
            raise Http404()

        qs = qs.annotate(
            no_folios=Count('pages', filter=Q(pages__source__isnull=False))
        )
        source = qs.first()
        pages = source.source_pages.all().values(
            pageId=F('page__pk'),
            pageName=F('page__name'),
            transcriptionId=F('transcription__pk')
        )

        context = self.get_context(request)
        context.update({
            'inventory': True,
            'set_id': self.source_set.id,
            'title': source.name,
            'data': {
                'folios': list(pages),
                **SourceSerializer(source).data,
            },
        })
        return TemplateResponse(
          request, 'dalme_public/inventory.html', context
        )

    @property
    def collection(self):
        return self.get_parent()

    @property
    def alias_type(self):
        try:
            return self.source_set.set_type
        except AttributeError:
            return None

    @property
    def sources(self):
        return self.source_set.members.all()

    def clean(self):
        if self.alias_type is not None and self.set_type != self.alias_type:
            mismatch = f'{self.set_type} != {self.alias_type}'
            raise ValidationError(
                f'{self._meta.model.__name__}.set_type mismatch: {mismatch}'
            )
        return super().clean()
