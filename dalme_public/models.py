"""Model dalme_public data."""
import contextlib
import json
import textwrap
from datetime import datetime, timedelta
from urllib import parse

from bs4 import BeautifulSoup as BSoup
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.embeds.blocks import EmbedBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import AbstractImage, AbstractRendition, Image
from wagtail.models import Orderable, Page
from wagtail.snippets.models import register_snippet
from wagtailmodelchooser import Chooser, register_model_chooser

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F
from django.db.models.functions import Coalesce
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.utils import timezone

from dalme_app.forms import SearchForm
from dalme_app.models import Collection as DalmeCollection
from dalme_app.models import SavedSearch
from dalme_app.utils import Search, SearchContext, formset_factory
from dalme_public import forms
from dalme_public.blocks import (
    AnnouncementBannerBlock,
    BibliographyBlock,
    CarouselBlock,
    ChartEmbedBlock,
    DocumentBlock,
    ExternalResourceBlock,
    FooterPageChooserBlock,
    FootnotesPlaceMarker,
    InlineImageBlock,
    MainImageBlock,
    PersonBlock,
    SocialBlock,
    SponsorBlock,
    SubsectionBlock,
    SubsectionEndMarkerBlock,
)
from dalme_public.serializers import PublicRecordSerializer
from ida.models import Record

# https://github.com/django/django/blob/3bc4240d979812bd11365ede04c028ea13fdc8c6/django/urls/converters.py#L26
UUID_RE = '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
FOLIO_RE = '[0-9a-z:]+'

HEADER_POSITION = (
    ('top', 'Top'),
    ('center', 'Center'),
    ('bottom', 'Bottom'),
)


@register_model_chooser
class RecordChooser(Chooser):
    model = Record
    modal_template = 'dalme_public/includes/_source_chooser_modal.html'

    def get_queryset(self, request):
        qs = Record.objects.filter(type=13, workflow__is_public=True).order_by('name')
        if request.GET.get('search'):
            qs = qs.filter(name__icontains=request.GET['search'])
        return qs


class SetFieldPanel(FieldPanel):
    def on_form_bound(self):
        qs = DalmeCollection.objects.filter(published=True)
        self.form.fields['source_set'].queryset = qs
        self.form.fields['source_set'].empty_label = '--------'
        super().on_form_bound()


class DALMEImage(AbstractImage):
    caption = models.CharField(max_length=255, null=True, blank=True)
    admin_form_fields = (*Image.admin_form_fields, 'caption')


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(DALMEImage, on_delete=models.CASCADE, related_name='renditions')

    class Meta:
        unique_together = ('image', 'filter_spec', 'focal_point_key')


@register_snippet
class Footer(models.Model):
    pages = StreamField([('page', FooterPageChooserBlock())], null=True, use_json_field=True)
    copyright = models.CharField(max_length=255, blank=True, null=True)  # noqa: A003
    social = StreamField([('social', SocialBlock())], null=True, use_json_field=True)

    panels = [
        FieldPanel('pages'),
        FieldPanel('copyright'),
        FieldPanel('social'),
    ]

    def __str__(self):
        return 'Site Footer'

    def clean(self):
        if self.id is None and self._meta.model.objects.exists():
            msg = 'The site can only have one footer.'
            raise ValidationError(msg)


@register_snippet
class SearchPage(models.Model):
    help_content = StreamField(
        [
            ('text', blocks.RichTextBlock()),
            ('html', blocks.RawHTMLBlock()),
        ],
        null=True,
        use_json_field=True,
    )

    header_image = models.ForeignKey(
        'dalme_public.DALMEImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='The image that will display in the header.',
    )

    header_position = models.CharField(
        max_length=6,
        choices=HEADER_POSITION,
        default='top',
        help_text='Position of the header image within its container.',
    )

    panels = [
        FieldPanel('header_image'),
        FieldPanel('header_position'),
        FieldPanel('help_content'),
    ]

    def __str__(self):
        return 'Search Page'

    def clean(self):
        if self.id is None and self._meta.model.objects.exists():
            msg = 'There can only be one search page.'
            raise ValidationError(msg)


@register_snippet
class ExplorePage(models.Model):
    text_before = StreamField(
        [
            ('text', blocks.RichTextBlock()),
            ('heading', blocks.CharBlock()),
            ('html', blocks.RawHTMLBlock()),
        ],
        null=True,
        use_json_field=True,
    )

    text_after = StreamField(
        [
            ('inline_image', InlineImageBlock()),
            ('text', blocks.RichTextBlock()),
            ('heading', blocks.CharBlock()),
            ('html', blocks.RawHTMLBlock()),
            ('embed', EmbedBlock(icon='media')),
        ],
        null=True,
        use_json_field=True,
    )

    header_image = models.ForeignKey(
        'dalme_public.DALMEImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='The image that will display in the header.',
    )

    header_position = models.CharField(
        max_length=6,
        choices=HEADER_POSITION,
        default='top',
        help_text='Position of the header image within its container.',
    )

    panels = [
        FieldPanel('header_image'),
        FieldPanel('header_position'),
        FieldPanel('text_before'),
        FieldPanel('text_after'),
    ]

    def __str__(self):
        return 'Explore Page Content'

    def clean(self):
        if self.id is None and self._meta.model.objects.exists():
            msg = 'There can only be one Explore page.'
            raise ValidationError(msg)


@register_snippet
class RecordBrowser(models.Model):
    header_image = models.ForeignKey(
        'dalme_public.DALMEImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='The image that will display in the header.',
    )

    header_position = models.CharField(
        max_length=6,
        choices=HEADER_POSITION,
        default='top',
        help_text='Position of the header image within its container.',
    )

    panels = [
        FieldPanel('header_image'),
        FieldPanel('header_position'),
    ]

    def __str__(self):
        return 'Record Browser'

    def clean(self):
        if self.id is None and self._meta.model.objects.exists():
            msg = 'There can only be one Record Browser page.'
            raise ValidationError(msg)


@register_snippet
class RecordViewer(models.Model):
    header_image = models.ForeignKey(
        'dalme_public.DALMEImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='The image that will display in the header.',
    )

    header_position = models.CharField(
        max_length=6,
        choices=HEADER_POSITION,
        default='top',
        help_text='Position of the header image within its container.',
    )

    panels = [
        FieldPanel('header_image'),
        FieldPanel('header_position'),
    ]

    def __str__(self):
        return 'Record Viewer'

    def clean(self):
        if self.id is None and self._meta.model.objects.exists():
            msg = 'There can only be one Record Viewer page.'
            raise ValidationError(msg)


class DALMEPage(Page):
    header_image = models.ForeignKey(
        'dalme_public.DALMEImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='The image that will display in the header.',
    )
    header_position = models.CharField(
        max_length=6,
        choices=HEADER_POSITION,
        default='top',
        help_text='Position of the header image within its container.',
    )
    short_title = models.CharField(
        max_length=63,
        null=True,
        blank=True,
        help_text='An optional short title that will be displayed in certain space constrained contexts.',
    )

    body = StreamField(
        [
            ('main_image', MainImageBlock()),
            ('carousel', CarouselBlock(ImageChooserBlock())),
            ('chart_embed', ChartEmbedBlock()),
            ('inline_image', InlineImageBlock()),
            ('text', blocks.RichTextBlock()),
            ('heading', blocks.CharBlock()),
            ('pullquote', blocks.RichTextBlock(icon='openquote')),
            ('page', blocks.PageChooserBlock()),
            ('bibliography', BibliographyBlock()),
            ('document', DocumentBlock()),
            ('person', PersonBlock()),
            ('external_resource', ExternalResourceBlock()),
            ('embed', EmbedBlock(icon='media')),
            ('html', blocks.RawHTMLBlock()),
            ('subsection', SubsectionBlock()),
            ('subsection_end_marker', SubsectionEndMarkerBlock()),
            ('footnotes_placemarker', FootnotesPlaceMarker()),
        ],
        null=True,
        use_json_field=True,
    )

    class Meta:
        abstract = True

    def get_context(self, request):
        context = super().get_context(request)
        context.update(
            {
                'header_image': self.header_image,
                'header_position': self.header_position,
            },
        )
        return context

    @property
    def main_image(self):
        try:
            field = next(field for field in self.body if field.block.name in ['carousel', 'main_image'])
        except StopIteration:
            return None
        if field.block.name == 'main_image':
            return field.value
        try:
            return field.value[0]
        except IndexError:
            return None

    @staticmethod
    def smart_truncate(content, length=25, suffix='...'):
        # credit: https://stackoverflow.com/questions/250357/truncate-a-string-without-ending-in-the-middle-of-a-word
        return content if len(content) <= length else ' '.join(content[: length + 1].split(' ')[0:-1]).rstrip() + suffix

    @property
    def title_switch(self):
        """Utility to reduce OR coalescing in templates.

        Prefer the short_title if a Page has one, if not fallback to title.

        """
        try:
            if self.short_title in ['Object', 'Essay', 'Inventory']:
                return self.smart_truncate(self.title)
        except AttributeError:
            return self.title
        else:
            return self.short_title or self.title


class FeaturedPage(DALMEPage):
    alternate_author = models.CharField(
        max_length=127,
        null=True,
        blank=True,
        help_text='An optional name field that will be displayed as the author of this page instead of the user who created it.',
    )

    citable = models.BooleanField(
        default=True,
        help_text='Check this box to show the "Cite" menu for this page.',
    )

    front_page_image = models.ForeignKey(
        'dalme_public.DALMEImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text='The image that will display on the front page.',
    )

    class Meta:
        abstract = True

    def get_context(self, request):
        context = super().get_context(request)
        context['feature_type'] = self.short_title
        return context

    @property
    def author(self):
        if self.alternate_author:
            return self.alternate_author
        return self.owner.profile.full_name

    @property
    def scheduled_publication(self):
        revisions = self.revisions.filter(approved_go_live_at__isnull=False).order_by('-created_at')
        if revisions.exists():
            return revisions.first().approved_go_live_at  # .strftime('%d-%b-%Y@%H:%M')
        return None

    @property
    def front_image(self):
        return self.front_page_image or self.main_image

    def snippet(self, width=200):
        try:
            text = next(field for field in self.body if field.block.name == 'text')
        except StopIteration:
            return ''
        return textwrap.shorten(
            BSoup(text.value.source, 'html.parser').get_text(),
            width=width,
            placeholder='...',
        )

    def resolve_source_url(self):
        raise NotImplementedError

    def clean(self):
        if self.go_live_at:
            qs = self._meta.model.objects.filter(
                go_live_at=self.go_live_at,
            ).exclude(pk=self.pk)
            if qs.exists():
                model = self._meta.label.split('.')[-1]
                title = qs.first().title
                msg = f'{model}: {title} is already scheduled for publication at: {self.go_live_at}'
                raise ValidationError(msg)

        if self.source_set and self.source:
            try:
                # TODO: There must be a better way to determine Set membership
                # than this but the (bi-directional) generic relations make it
                # tough. UPDATE 2023: Can't we just do this?
                #
                # if not self.source_set.members.filter(content_object__pk=self.source.pk).exists():
                #     msg = f'{self.source} is not a member of: {self.source_set}'
                #     raise ValidationError(msg) from exc
                # return super().clean()
                #
                # Let's capture it with a regression test and see.
                next(
                    source.content_object
                    for source in self.source_set.members.all()
                    if source.content_object.pk == self.source.pk
                )
            except StopIteration as exc:
                msg = f'{self.source} is not a member of: {self.source_set}'
                raise ValidationError(msg) from exc

        return super().clean()


class Home(DALMEPage):
    template = 'home.html'

    learn_more_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    sponsors = StreamField([('sponsors', SponsorBlock())], null=True, use_json_field=True)
    banners = StreamField([('banners', AnnouncementBannerBlock())], null=True, use_json_field=True)

    subpage_types = [
        'dalme_public.Section',
        'dalme_public.Features',
        'dalme_public.Collections',
    ]

    content_panels = [
        *DALMEPage.content_panels,
        FieldPanel('header_image'),
        FieldPanel('learn_more_page'),
        FieldPanel('banners'),
        FieldPanel('body'),
        FieldPanel('sponsors'),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        objects = FeaturedObject.objects.live().specific().order_by('go_live_at')
        inventories = FeaturedInventory.objects.live().specific().order_by('go_live_at')
        essays = Essay.objects.live().specific().order_by('go_live_at')

        context['featured_object'] = objects.last()
        context['featured_inventory'] = inventories.last()
        context['essay'] = essays.last()

        return context


class Section(DALMEPage):
    parent_page_types = ['dalme_public.Home']
    subpage_types = [
        'dalme_public.Flat',
        'dalme_public.Bibliography',
    ]

    content_panels = [*DALMEPage.content_panels, FieldPanel('short_title')]


class Flat(DALMEPage):
    show_contact_form = models.BooleanField(
        default=False,
        help_text='Check this box to show a contact form on the page.',
    )

    citable = models.BooleanField(
        default=False,
        help_text='Check this box to show the "Cite" menu for this page.',
    )

    parent_page_types = [
        'dalme_public.Section',
        'dalme_public.Collection',
        'dalme_public.Flat',
        'dalme_public.Collections',
    ]
    subpage_types = ['dalme_public.Flat']

    content_panels = [
        *DALMEPage.content_panels,
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
                'dalme_public/flat.html',
                {'page': self, 'form': form},
            )

        return super().serve(request)


class Features(DALMEPage):
    parent_page_types = ['dalme_public.Home']
    subpage_types = [
        'dalme_public.FeaturedObject',
        'dalme_public.FeaturedInventory',
        'dalme_public.Essay',
    ]

    content_panels = [
        *DALMEPage.content_panels,
        FieldPanel('header_image'),
        FieldPanel('header_position'),
        FieldPanel('short_title'),
        FieldPanel('body'),
    ]

    def get_context(self, request):
        from dalme_public.filters import FeaturedFilter

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


class Bibliography(DALMEPage):
    parent_page_types = ['dalme_public.Section']
    subpage_types = ['dalme_public.Flat']

    content_panels = [
        *DALMEPage.content_panels,
        FieldPanel('header_image'),
        FieldPanel('header_position'),
        FieldPanel('short_title'),
        FieldPanel('body'),
    ]


class FeaturedObject(FeaturedPage):
    short_title = 'Object'
    source = models.ForeignKey(
        'ida.Record',
        related_name='featured_objects',
        on_delete=models.SET_NULL,
        null=True,
    )
    source_set = models.ForeignKey(
        'dalme_app.Collection',
        related_name='featured_objects',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='Optional, select a particular public set for the source associated with this object. The source must be a member of the set chosen or the page will not validate.',
    )

    parent_page_types = ['dalme_public.Features']
    subpage_types = []
    template = 'dalme_public/feature.html'

    content_panels = [
        *DALMEPage.content_panels,
        FieldPanel('header_image'),
        FieldPanel('header_position'),
        FieldPanel('front_page_image'),
        FieldPanel('source'),
        SetFieldPanel('source_set'),
        FieldPanel('alternate_author'),
        FieldPanel('citable'),
        FieldPanel('body'),
    ]

    class Meta:
        verbose_name = 'Object'
        verbose_name_plural = 'Objects'


class FeaturedInventory(FeaturedPage):
    short_title = 'Inventory'
    source = models.ForeignKey(
        'ida.Record',
        related_name='featured_inventories',
        on_delete=models.SET_NULL,
        null=True,
    )
    source_set = models.ForeignKey(
        'dalme_app.Collection',
        related_name='featured_inventories',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='Optional, select a particular public set for the source associated with this inventory. The source must be a member of the set chosen or the page will not validate.',
    )

    parent_page_types = ['dalme_public.Features']
    subpage_types = []
    template = 'dalme_public/feature.html'

    content_panels = [
        *DALMEPage.content_panels,
        FieldPanel('header_image'),
        FieldPanel('header_position'),
        FieldPanel('front_page_image'),
        FieldPanel('source'),
        SetFieldPanel('source_set'),
        FieldPanel('alternate_author'),
        FieldPanel('citable'),
        FieldPanel('body'),
    ]

    class Meta:
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventories'


class Essay(FeaturedPage):
    short_title = 'Essay'
    source = models.ForeignKey(
        'ida.Record',
        related_name='essays',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    source_set = models.ForeignKey(
        'dalme_app.Collection',
        related_name='essays',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='Optional, select a particular public set for the source associated with this essay. The source must be a member of the set chosen or the page will not validate.',
    )

    parent_page_types = ['dalme_public.Features']
    subpage_types = []
    template = 'dalme_public/feature.html'

    content_panels = [
        *DALMEPage.content_panels,
        FieldPanel('header_image'),
        FieldPanel('header_position'),
        FieldPanel('front_page_image'),
        FieldPanel('source'),
        SetFieldPanel('source_set'),
        FieldPanel('alternate_author'),
        FieldPanel('citable'),
        FieldPanel('body'),
    ]

    class Meta:
        verbose_name = 'Mini Essay'
        verbose_name_plural = 'Mini Essays'


class Corpus(Orderable, ClusterableModel):
    title = models.CharField(max_length=255)
    description = RichTextField()

    page = ParentalKey('dalme_public.Collections', related_name='corpora')
    collections = ParentalManyToManyField(
        'dalme_public.Collection',
        related_name='corpora',
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('collections'),
    ]

    def __str__(self):
        return self.title


class SearchEnabled(RoutablePageMixin, DALMEPage):
    class Meta:
        abstract = True

    @route(r'^search/$', name='search')
    @route(rf'^search/({UUID_RE})/$', name='saved_search')
    def search(self, request, pk=None):
        context = self.get_context(request)
        search_context = SearchContext(public=True)
        search_formset = formset_factory(SearchForm)
        search_snippet = SearchPage.objects.first()

        context.update(
            {
                'header_image': search_snippet.header_image,
                'header_position': search_snippet.header_position,
                'query': False,
                'advanced': False,
                'form': search_formset(form_kwargs={'fields': search_context.fields}),
                'results': [],
                'paginator': {},
                'errors': False,
                'paginated': False,
                'suggestion': None,
                'search': True,
                'search_context': search_context.context,
            },
        )

        if pk:
            saved_search = SavedSearch.objects.filter(id=pk)
            if saved_search.exists():
                saved_search = json.loads(saved_search.first().search)
                saved_search.pop('csrfmiddlewaretoken')
                saved_search['form-SAVE'] = ''
                request.POST = saved_search
                request.method = 'POST'

        if request.method != 'POST' and request.session.get('public-search-post', False):
            seconds = 86401
            default_ts = datetime.timestamp(
                datetime.now(tz=timezone.get_current_timezone()) - timedelta(seconds=seconds),
            )
            stored_dt = datetime.fromtimestamp(
                request.session.get('public-search-ts', default_ts),
                tz=timezone.get_current_timezone(),
            )
            delta = datetime.now(tz=timezone.get_current_timezone()) - stored_dt
            if delta.seconds < seconds:
                request.POST = request.session['public-search-post']
                request.method = 'POST'

        if request.method == 'POST':
            formset = search_formset(request.POST, form_kwargs={'fields': search_context.fields})
            request.session['public-search-post'] = request.POST
            request.session['public-search-ts'] = datetime.timestamp(
                datetime.now(tz=timezone.get_current_timezone()),
            )
            if formset.is_valid():
                search_obj = Search(
                    data=formset.cleaned_data,
                    public=True,
                    page=request.POST.get('form-PAGE', 1),
                    highlight=True,
                    search_context=search_context.context,
                )
                context.update(
                    {
                        'query': True,
                        'advanced': formset.cleaned_data[0].get('field_value', '') != '',
                        'form': formset,
                        'results': search_obj.results,
                        'paginator': search_obj.paginator,
                        'errors': search_obj.errors,
                        'paginated': search_obj.paginator.get('num_pages', 0) > 1,
                    },
                )

        return render(
            request,
            'dalme_public/search.html',
            context,
        )

    @route(r'^records/$', name='records')
    def records(self, request, scoped=True):  # noqa: ARG002
        context = self.get_context(request)
        browser_snippet = RecordBrowser.objects.first()

        context.update(
            {
                'header_image': browser_snippet.header_image,
                'header_position': browser_snippet.header_position,
                'records': True,
                'browse_mode': request.session.get('public-browse-mode', 'wide'),
            },
        )

        with contextlib.suppress(AttributeError):
            context.update({'set_id': self.source_set.id})

        return TemplateResponse(
            request,
            'dalme_public/records.html',
            context,
        )

    @route(rf'^records/({UUID_RE})/$', name='record')
    @route(rf'^records/({UUID_RE})/({FOLIO_RE})/$', name='record_folio')
    def record(self, request, pk, folio=None, scoped=True):  # noqa: ARG002
        qs = Record.objects.filter(pk=pk)
        if not qs.exists():
            raise Http404

        source = qs.first()
        as_preview = self.preview if hasattr(self, 'preview') else False

        if not source.workflow.is_public and not as_preview:
            raise Http404

        pages = (
            source.folios.all()
            .values(
                pageId=F('page__pk'),
                pageName=F('page__name'),
                transcriptionId=F('transcription__pk'),
                pageOrder=F('page__order'),
                pageImageId=F('page__dam_id'),
            )
            .order_by('pageOrder')
        )

        initial_folio_index = (
            next(
                (i for i, item in enumerate(pages) if item['pageName'] == folio),
                0,
            )
            if folio
            else 0
        )

        context = self.get_context(request)
        viewer_snippet = RecordViewer.objects.first()

        from_search = False
        if request.META.get('HTTP_REFERER') and 'search' in request.META.get('HTTP_REFERER'):
            from_search = True

        data = PublicRecordSerializer(source).data
        purl = f'https://purl.dalme.org/{source.id}/' if as_preview else source.get_purl()

        context.update(
            {
                'header_image': viewer_snippet.header_image,
                'header_position': viewer_snippet.header_position,
                'record': True,
                'from_search': from_search,
                'viewer_mode': request.session.get('public-viewer-mode', 'vertical-split'),
                'render_mode': request.session.get('public-render-mode', 'scholarly'),
                'purl': purl,
                'title': self.smart_truncate(data['name'], length=35),
                'data': {
                    'folios': list(pages),
                    **data,
                },
                'initial_folio_index': initial_folio_index,
            },
        )

        with contextlib.suppress(AttributeError):
            context.update({'set_id': self.source_set.id})

        return TemplateResponse(
            request,
            'dalme_public/record.html',
            context,
        )

    def relative_url(self, current_site, request=None):
        if hasattr(request, 'is_dummy') and request.is_dummy:
            return '/'
        return self.get_url(request=request, current_site=current_site)


class Collections(SearchEnabled):
    citable = models.BooleanField(
        default=True,
        help_text='Check this box to show the "Cite" menu for this page.',
    )

    parent_page_types = ['dalme_public.Home']
    subpage_types = [
        'dalme_public.Collection',
        'dalme_public.Flat',
    ]

    content_panels = [
        *DALMEPage.content_panels,
        FieldPanel('header_image'),
        FieldPanel('header_position'),
        FieldPanel('short_title'),
        FieldPanel('citable'),
        FieldPanel('body'),
        MultiFieldPanel([InlinePanel('corpora', min_num=1, label='Corpus')], heading='Corpora'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['corpora'] = [(corpus, corpus.collections.all()) for corpus in self.corpora.all()]
        return context

    @route(r'^explore/$', name='explore')
    def explore(self, request):
        context = self.get_context(request)
        explorer_snippet = ExplorePage.objects.first()

        context.update(
            {
                'header_image': explorer_snippet.header_image,
                'header_position': explorer_snippet.header_position,
                'explore': True,
            },
        )

        return TemplateResponse(
            request,
            'dalme_public/explore.html',
            context,
        )


class Collection(SearchEnabled):
    source_set = models.ForeignKey(
        'dalme_app.Collection',
        related_name='public_collections',
        on_delete=models.PROTECT,
    )
    citable = models.BooleanField(
        default=True,
        help_text='Check this box to show the "Cite" menu for this page.',
    )
    preview = models.BooleanField(
        default=False,
        help_text='Check this box to set this collection to Preview mode only. It will be made public but not added to the search or map. Only people with the link will be able to access it.',
    )
    parent_page_types = ['dalme_public.Collections']
    subpage_types = ['dalme_public.Flat']

    content_panels = [
        *DALMEPage.content_panels,
        SetFieldPanel('source_set'),
        FieldPanel('header_image'),
        FieldPanel('header_position'),
        FieldPanel('citable'),
        FieldPanel('preview'),
        FieldPanel('body'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        if request.META.get('HTTP_REFERER'):
            params = dict(parse.parse_qsl(parse.urlsplit(request.META.get('HTTP_REFERER')).query))
            if 'collection' in params:
                context['collection'] = params['collection']
        return context

    @property
    def stats(self):
        if self.preview:
            stats_dict = {
                'records': self.source_set.member_count,
                'languages': self.source_set.get_languages(),
                'coverage': self.source_set.get_time_coverage(),
            }
        else:
            stats_dict = {
                'records': self.source_set.get_public_member_count(),
                'languages': self.source_set.get_public_languages(),
                'coverage': self.source_set.get_public_time_coverage(),
            }

        if self.source_set.stat_title is not None:
            stats_dict['other'] = {'label': self.source_set.stat_title, 'text': self.source_set.stat_text}

        return stats_dict

    @property
    def count(self):
        return self.source_set.member_count(published=True)

    @property
    def sources(self):
        return self.source_set.members.all()

    def clean(self):
        if self.source_set:
            self.slug = self.source_set.name.replace(' ', '-').lower()
        return super().clean()
