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

from public.extensions.extras.blocks.defaults import DEFAULT_TABLE_OPTIONS
from public.extensions.extras.blocks.document import DocumentBlock
from public.extensions.extras.blocks.subsection import SubsectionBlock
from public.extensions.extras.blocks.text_expandable import TextExpandableBlock
from public.extensions.images.blocks import InlineImageBlock, MainImageBlock
from public.extensions.team.blocks import TeamListBlock
from public.extensions.team.models import TeamMember
from public.models.base_page import BasePage

BLOCK_SET = [
    ('document', DocumentBlock()),
    ('heading', blocks.CharBlock()),
    ('inline_image', InlineImageBlock()),
    ('main_image', MainImageBlock()),
    ('page', blocks.PageChooserBlock()),
    ('pullquote', blocks.RichTextBlock(icon='openquote')),
    ('subsection', SubsectionBlock()),
    ('table', TableBlock(table_options=DEFAULT_TABLE_OPTIONS)),
    ('team_list', TeamListBlock()),
    ('text', blocks.RichTextBlock()),
    ('text_expandable', TextExpandableBlock()),
]


class People(RoutablePageMixin, BasePage):
    template = 'public/flat.html'

    body = StreamField(BLOCK_SET, null=True)

    parent_page_types = [
        'public.Section',
        'public.Collection',
        'public.Flat',
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

        contributions = [
            {'record': r.target, 'credit': r.scopes.first().parameters['credit']}
            for r in person.user.person_record.agent_ptr.relationships_as_source.filter(
                Q(rel_type__short_name='authorship')
                & (
                    Q(scopes__parameters__credit='editor')
                    | Q(scopes__parameters__credit='contributor')
                    | Q(scopes__parameters__credit='corrections')
                )
            )
        ]

        context = self.get_context(request)
        context.update(
            {
                'title': person.name,
                'person': person,
                'contributions': contributions,
            }
        )

        return TemplateResponse(
            request,
            'public/person.html',
            context,
        )
