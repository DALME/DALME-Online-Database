"""Model for people list page."""

from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.fields import StreamField

from django.db.models import Q, Value
from django.db.models.functions import Lower, Replace
from django.http import Http404
from django.template.response import TemplateResponse

from web.extensions.extras.blocks.defaults import DEFAULT_TABLE_OPTIONS
from web.extensions.extras.blocks.document import DocumentBlock
from web.extensions.extras.blocks.subsection import SubsectionBlock
from web.extensions.images.blocks import InlineImageBlock
from web.extensions.team.blocks import TeamListBlock
from web.extensions.team.models import TeamMember
from web.models import BasePage, Essay, FeaturedInventory, FeaturedObject

BLOCK_SET = [
    ('document', DocumentBlock()),
    ('heading', blocks.CharBlock()),
    ('inline_image', InlineImageBlock()),
    ('page', blocks.PageChooserBlock()),
    ('pullquote', blocks.RichTextBlock(icon='openquote', editor='minimal')),
    ('subsection', SubsectionBlock()),
    ('table', TableBlock(table_options=DEFAULT_TABLE_OPTIONS, icon='table-cells', form_classname='table-block')),
    ('team_list', TeamListBlock()),
    ('text', blocks.RichTextBlock(editor='minimal')),
]


class People(RoutablePageMixin, BasePage):
    template = 'flat.html'

    body = StreamField(BLOCK_SET, null=True)

    parent_page_types = [
        'web.Section',
        'web.Collection',
        'web.Flat',
    ]
    page_description = 'A page designed to showcase one or many people lists.'

    metadata_panels = [
        *BasePage.metadata_panels,
        FieldPanel('short_title'),
    ]

    @path('<slug:name_slug>/', name='people')
    def person(self, request, name_slug):
        qs = TeamMember.objects.annotate(name_slug=Replace(Lower('name'), Value(' '), Value('-'))).filter(
            name_slug=name_slug
        )
        if not qs.exists():
            raise Http404

        person = qs.get()

        contributions = sorted(
            [
                {
                    'record': r.target,
                    'credit': r.scopes.first().parameters['credit'],
                    'month': r.target.modification_timestamp.strftime('%b'),
                    'year': r.target.modification_timestamp.year,
                }
                for r in person.user.person_record.agent_ptr.relationships_as_source.filter(
                    Q(rel_type__short_name='authorship')
                    & (
                        Q(scopes__parameters__credit='editor')
                        | Q(scopes__parameters__credit='contributor')
                        | Q(scopes__parameters__credit='corrections')
                    )
                )
                if r.target
            ],
            key=lambda x: x['record'].modification_timestamp,
            reverse=True,
        )

        q = Q(authors=person.user) | (Q(byline_text__isnull=True) & Q(owner=person.user))
        features = [
            {'title': i.title, 'url': i.url, 'month': i.go_live_at.strftime('%b'), 'year': i.go_live_at.year}
            for i in FeaturedInventory.objects.filter(q)
            .union(
                FeaturedObject.objects.filter(q),
                Essay.objects.filter(q),
            )
            .order_by('-go_live_at')
        ]

        context = self.get_context(request)
        context.update(
            {
                'title': person.name,
                'person': person,
                'contributions': contributions,
                'features': features,
            }
        )

        return TemplateResponse(
            request,
            'person.html',
            context,
        )
