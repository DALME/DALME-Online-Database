"""Model for people list page."""

from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path

from django.db.models import Q, Value
from django.db.models.functions import Lower, Replace
from django.http import Http404
from django.template.response import TemplateResponse

from web.extensions.block_registry import RegistryStreamField
from web.extensions.team.models import TeamMember
from web.models import BasePage, Essay, FeaturedInventory, FeaturedObject

STREAMFIELD_INTERFACE = [
    'document',
    'heading',
    'inline_image',
    'page',
    'pullquote',
    'subsection',
    'table',
    'team_list',
    'text',
]


class People(RoutablePageMixin, BasePage):
    template = 'web/flat.html'

    body = RegistryStreamField(STREAMFIELD_INTERFACE, null=True)

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
        qs = TeamMember.objects.annotate(
            name_slug=Replace(Replace(Lower('name'), Value(' '), Value('-')), Value('.'))
        ).filter(name_slug=name_slug)
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
        feature_qs = (
            FeaturedInventory.objects.live()
            .filter(q)
            .union(
                FeaturedObject.objects.live().filter(q),
                Essay.objects.live().filter(q),
            )
            .order_by('-go_live_at')
        )

        features = (
            [
                {'title': i.title, 'url': i.url, 'month': i.go_live_at.strftime('%b'), 'year': i.go_live_at.year}
                for i in feature_qs
            ]
            if feature_qs.exists()
            else []
        )

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
            'web/person.html',
            context,
        )
