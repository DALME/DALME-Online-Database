import textwrap

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Count, F, Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse

from bs4 import BeautifulSoup as BSoup
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
)
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core import blocks, hooks
from wagtail.core.models import Orderable, Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail.snippets.models import register_snippet
from wagtailmodelchooser import register_model_chooser, Chooser
from wagtailmodelchooser.edit_handlers import ModelChooserPanel

from dalme_app.models import Set as DALMESet, Source
from dalme_app.web_serializers import RecordSerializer
from dalme_public import forms
from dalme_public.blocks import (
    CarouselBlock,
    DocumentBlock,
    ExternalResourceBlock,
    MainImageBlock,
    PersonBlock,
    SponsorBlock,
    SubsectionBlock,
)


# https://github.com/django/django/blob/3bc4240d979812bd11365ede04c028ea13fdc8c6/django/urls/converters.py#L26
UUID_RE = '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'


@hooks.register('before_serve_page')
def redirects(page, request, serve_args, serve_kwargs):
    if page.is_root():
        home = page.get_children().live().first()
        return redirect(home.url, permanent=False)
    if page._meta.label == 'dalme_public.Section':
        url = page.get_children().live().first().url
        return redirect(url, permanent=False)


@register_model_chooser
class SourceChooser(Chooser):
    model = Source

    def get_queryset(self, request):
        qs = super().get_queryset(request).order_by('name')
        if request.GET.get('q'):
            qs = qs.filter(name__icontains=request.GET['q'])
        return qs


class SetFieldPanel(FieldPanel):
    def on_form_bound(self):
        qs = DALMESet.objects.filter(set_type=DALMESet.COLLECTION)
        self.form.fields['source_set'].queryset = qs
        self.form.fields['source_set'].empty_label = '--------'
        super().on_form_bound()


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


@register_snippet
class Footer(models.Model):
    pages = StreamField([
        ('page', blocks.PageChooserBlock()),
    ])

    panels = [StreamFieldPanel('pages')]

    def __str__(self):
        return "Site Footer"

    def clean(self):
        if self._meta.model.objects.exists():
            raise ValidationError('The site can only have one footer.')


class DALMEPage(Page):
    header_image = models.ForeignKey(
        'dalme_public.DALMEImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='The image that will display in the header.'
    )
    short_title = models.CharField(
        max_length=63,
        null=True,
        blank=True,
        help_text='An optional short title that will be displayed in certain contexts.'  # noqa
    )

    body = StreamField([
        ('main_image', MainImageBlock()),
        ('carousel', CarouselBlock(ImageChooserBlock())),
        ('inline_image', ImageChooserBlock()),
        ('text', blocks.RichTextBlock()),
        ('heading', blocks.CharBlock()),
        ('pullquote', blocks.RichTextBlock(icon='openquote')),
        ('page', blocks.PageChooserBlock()),
        ('document', DocumentBlock()),
        ('person', PersonBlock()),
        ('external_resource', ExternalResourceBlock()),
        ('embed', EmbedBlock(icon='media')),
        ('html', blocks.RawHTMLBlock()),
        ('subsection', SubsectionBlock()),
    ], null=True)

    class Meta:
        abstract = True

    @property
    def main_image(self):
        try:
            field = next(
                field for field in self.body
                if field.block.name in ['carousel', 'main_image']
            )
        except StopIteration:
            return None
        if field.block.name == 'main_image':
            return field.value
        try:
            return field.value[0]
        except IndexError:
            return None

    @property
    def title_switch(self):
        """Utility to reduce OR coalescing in templates.
        Prefer the short_title if a Page has one, if not fallback to title.
        """
        try:
            return self.short_title or self.title
        except AttributeError:
            return self.title


class FeaturedPage(DALMEPage):
    alternate_author = models.CharField(
        max_length=127,
        null=True,
        blank=True,
        help_text='An optional name field that will be displayed as the author of this page instead of the user who created it.'  # noqa
    )

    class Meta:
        abstract = True

    @property
    def author(self):
        if self.alternate_author:
            return self.alternate_author
        return f'{self.owner.first_name} {self.owner.last_name}'

    def snippet(self, width=200):
        try:
            text = next(
                field for field in self.body
                if field.block.name == 'text'
            )
        except StopIteration:
            return ''
        return textwrap.shorten(
            BSoup(text.value.source, 'html.parser').get_text(),
            width=width,
            placeholder=' [...]'
        )

    def resolve_source_url(self):
        raise NotImplementedError()

    def clean(self):
        if self.go_live_at:
            qs = self._meta.model.objects.filter(
                go_live_at=self.go_live_at
            ).exclude(pk=self.pk)
            if qs.exists():
                model = self._meta.label.split('.')[-1]
                title = qs.first().title
                raise ValidationError(
                    f'{model}: {title} is already scheduled for publication at: {self.go_live_at}'  # noqa
                )

        if self.source_set and not self.source:
            raise ValidationError(
                'You must specify a source in order to also specify a source set.'  # noqa
            )

        if self.source_set:
            try:
                # TODO: There must be a better way to determine Set membership
                # than this but the (bi-directional) generic relations make it
                # tough.
                next(
                    source.content_object
                    for source in self.source_set.members.all()
                    if source.content_object.pk == self.source.pk
                )
            except StopIteration:
                raise ValidationError(
                    f'{self.source} is not a member of: {self.source_set}'
                )
        return super().clean()


class Home(DALMEPage):
    sponsors = StreamField([
        ('sponsors', SponsorBlock()),
    ], null=True)

    subpage_types = [
        'dalme_public.Section',
        'dalme_public.Features',
        'dalme_public.Collections'
    ]

    content_panels = DALMEPage.content_panels + [
        ImageChooserPanel('header_image'),
        StreamFieldPanel('body'),
        StreamFieldPanel('sponsors'),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        objects = FeaturedObject.objects.live().order_by('-first_published_at')
        inventories = FeaturedInventory.objects.live().order_by(
            '-first_published_at'
        )
        essays = Essay.objects.live().order_by('-first_published_at')

        context['featured_object'] = objects.last()
        context['featured_inventory'] = inventories.last()
        context['essay'] = essays.last()
        return context


class Section(DALMEPage):
    parent_page_types = ['dalme_public.Home']
    subpage_types = ['dalme_public.Flat']

    content_panels = DALMEPage.content_panels + [
        FieldPanel('short_title'),
    ]


class Flat(DALMEPage):
    show_contact_form = models.BooleanField(
        default=False,
        help_text='Check this box to show a contact form on the page.'
    )

    parent_page_types = ['dalme_public.Section', 'dalme_public.Collection']
    subpage_types = []

    content_panels = DALMEPage.content_panels + [
        ImageChooserPanel('header_image'),
        FieldPanel('short_title'),
        FieldPanel('show_contact_form'),
        StreamFieldPanel('body'),
    ]

    def serve(self, request):
        if self.show_contact_form:
            form = forms.ContactForm(label_suffix='')
            if request.method == 'POST':
                form = forms.ContactForm(request.POST, label_suffix='')
                if form.is_valid():
                    form.save()
                    messages.success(
                        request, 'Your message has been delivered.'
                    )
                    return HttpResponseRedirect(self.url)
            return render(
                request, 'dalme_public/flat.html', {'page': self, 'form': form}
            )
        return super().serve(request)


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
        StreamFieldPanel('body'),
    ]

    def get_context(self, request):
        from dalme_public.filters import FeaturedFilter
        context = super().get_context(request)
        filtered = FeaturedFilter(
            request.GET,
            queryset=self.get_children().live().specific().order_by(
                '-first_published_at'
            )
        )
        context['featured'] = filtered.qs
        return context


class FeaturedObject(FeaturedPage):
    short_title = 'Object'
    source = models.ForeignKey(
        'dalme_app.Source',
        related_name='featured_objects',
        on_delete=models.PROTECT
    )
    source_set = models.ForeignKey(
        'dalme_app.Set',
        related_name='featured_objects',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text='Optional, select a particular public set for the source associated with this object. The source must be a member of the set chosen or the page will not validate.'  # noqa
    )

    parent_page_types = ['dalme_public.Features']
    subpage_types = []

    content_panels = DALMEPage.content_panels + [
        ImageChooserPanel('header_image'),
        ModelChooserPanel('source'),
        SetFieldPanel('source_set'),
        FieldPanel('alternate_author'),
        StreamFieldPanel('body'),
    ]

    class Meta:
        verbose_name = 'Object'
        verbose_name_plural = 'Objects'


class FeaturedInventory(FeaturedPage):
    short_title = 'Inventory'
    source = models.ForeignKey(
        'dalme_app.Source',
        related_name='featured_inventories',
        on_delete=models.PROTECT
    )
    source_set = models.ForeignKey(
        'dalme_app.Set',
        related_name='featured_inventories',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text='Optional, select a particular public set for the source associated with this inventory. The source must be a member of the set chosen or the page will not validate.'  # noqa
    )

    parent_page_types = ['dalme_public.Features']
    subpage_types = []

    content_panels = DALMEPage.content_panels + [
        ImageChooserPanel('header_image'),
        ModelChooserPanel('source'),
        SetFieldPanel('source_set'),
        FieldPanel('alternate_author'),
        StreamFieldPanel('body'),
    ]

    class Meta:
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventories'


class Essay(FeaturedPage):
    short_title = 'Essay'
    source = models.ForeignKey(
        'dalme_app.Source',
        related_name='essays',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    source_set = models.ForeignKey(
        'dalme_app.Set',
        related_name='essays',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text='Optional, select a particular public set for the source associated with this essay. The source must be a member of the set chosen or the page will not validate.'  # noqa
    )

    parent_page_types = ['dalme_public.Features']
    subpage_types = []

    content_panels = DALMEPage.content_panels + [
        ImageChooserPanel('header_image'),
        FieldPanel('source'),
        SetFieldPanel('source_set'),
        FieldPanel('alternate_author'),
        StreamFieldPanel('body'),
    ]

    class Meta:
        verbose_name = 'Mini Essay'
        verbose_name_plural = 'Mini Essays'


class Corpus(Orderable, ClusterableModel):
    title = models.CharField(max_length=255)
    description = RichTextField()

    page = ParentalKey('dalme_public.Collections', related_name='corpora')
    collections = ParentalManyToManyField(
        'dalme_public.Collection', related_name='corpora'
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('collections'),
    ]

    def __str__(self):
        return self.title


class Collections(RoutablePageMixin, DALMEPage):
    parent_page_types = ['dalme_public.Home']
    subpage_types = ['dalme_public.Collection']

    content_panels = DALMEPage.content_panels + [
        ImageChooserPanel('header_image'),
        FieldPanel('short_title'),
        StreamFieldPanel('body'),
        MultiFieldPanel(
            [InlinePanel('corpora', min_num=1, label='Corpus')],
            heading='Corpora',
        ),
    ]

    @route(r'^inventories/$', name='unscoped_inventories')
    def inventories(self, request):
        context = self.get_context(request)
        context.update({'inventories': True})
        return TemplateResponse(
          request, 'dalme_public/inventories.html', context
        )

    @route(rf'^inventories/({UUID_RE})/$', name='unscoped_inventory')
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
            'title': source.name,
            'data': {
                'folios': list(pages),
                **RecordSerializer(source).data,
            },
        })
        return TemplateResponse(
          request, 'dalme_public/inventory.html', context
        )

    def get_context(self, request):
        context = super().get_context(request)
        if request.GET.get('q'):
            corpora = []
            cls = self._meta.model.collection.related.related_model
            qs = cls.objects.filter(title__icontains=request.GET['q'])
            for collection in qs:
                for corpus in collection.corpora.all():
                    try:
                        data = next(
                            item for item in corpora if item[0] == corpus
                        )
                    except StopIteration:
                        corpora.append([corpus, [collection]])
                    else:
                        data[1].append(collection)
        else:
            corpora = [
                (corpus, corpus.collections.all())
                for corpus in self.corpora.all()
            ]

        context['corpora'] = corpora
        return context


class Collection(RoutablePageMixin, DALMEPage):
    set_type = DALMESet.COLLECTION
    source_set = models.ForeignKey(
        'dalme_app.Set',
        related_name='public_collections',
        on_delete=models.PROTECT
    )

    parent_page_types = ['dalme_public.Collections']
    subpage_types = ['dalme_public.Flat']

    content_panels = DALMEPage.content_panels + [
        SetFieldPanel('source_set'),
        ImageChooserPanel('header_image'),
        StreamFieldPanel('body'),
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
                **RecordSerializer(source).data,
            },
        })
        return TemplateResponse(
          request, 'dalme_public/inventory.html', context
        )

    @property
    def stats(self):
        status = 'Extensive range, with numerous inventories of artisans and low-status individuals.'  # noqa
        return {
            'inventories': self.source_set.get_public_member_count,
            'languages': self.source_set.get_languages,
            'coverage': self.source_set.get_time_coverage,
            'status': status,
        }

    @property
    def count(self):
        return self.source_set.get_public_member_count

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
