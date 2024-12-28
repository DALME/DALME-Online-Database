"""Create entries necessary for new data schemas."""

from django_tenants.utils import schema_context
from wagtail.log_actions import log

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import connection, transaction

from domain.models import (
    Collection,
    CollectionMembership,
    PreferenceKey,
    Project,
    ZoteroCollection,
)
from tenants.models import Tenant

from .base import BaseStage


class Stage(BaseStage):
    """Fixes after finishing all data migrations."""

    name = '12 Content fixes'

    @transaction.atomic
    def apply(self):
        """Execute the stage."""
        self.adjust_id_columns()
        self.create_project_and_library_entries()
        self.update_footnote_state()
        self.fix_biblio_page()
        self.replace_about_people()
        self.process_images()
        self.add_default_preferences()
        self.migrate_corpora()

    @transaction.atomic
    def adjust_id_columns(self):
        """Adjust autogenerated id sequences."""
        app_labels = [
            ('dalme', 'taggit'),
            ('dalme', 'wagtailadmin'),
            ('dalme', 'wagtailcore'),
            ('dalme', 'wagtaildocs'),
            ('dalme', 'wagtailembeds'),
            ('dalme', 'wagtailforms'),
            ('dalme', 'wagtailimages'),
            ('dalme', 'wagtailredirects'),
            ('public', 'wagtailusers'),
            ('dalme', 'web'),
            ('dalme', 'webimages'),
        ]

        for schema, app in app_labels:
            self.logger.info('Adjusting autogenerated id sequences for "%s" models', app)
            app_config = apps.get_app_config(app)
            if app_config.models_module is not None:
                for model in app_config.get_models():
                    model_name = model.__name__.lower()
                    qualified_name = f'{app}_{model_name}'
                    self.logger.info('Processing "%s"', qualified_name)

                    with connection.cursor() as cursor:
                        cursor.execute(f'SELECT * FROM {schema}.{qualified_name};')
                        rows = self.map_rows(cursor)
                        id_list = [int(row['id']) for row in rows if row.get('id')]
                        if id_list:
                            new_seq_start = max(id_list) + 1
                            cursor.execute(
                                f'ALTER TABLE {schema}.{qualified_name} ALTER COLUMN id RESTART WITH {new_seq_start};'
                            )

    @transaction.atomic
    def create_project_and_library_entries(self):
        # DALME
        self.logger.info('Creating project and library entries for DALME')
        collections = [
            {
                'id': 'A4QHN348',
                'label': 'Editions',
                'has_biblio_sources': True,
            },
            {
                'id': 'BKW2PVCM',
                'label': 'Glossaries and dictionaries',
                'has_biblio_sources': False,
            },
            {
                'id': 'QM9AZNT3',
                'label': 'Methodology',
                'has_biblio_sources': False,
            },
            {
                'id': 'SLIT6LID',
                'label': 'Studies',
                'has_biblio_sources': False,
            },
            {
                'id': 'FRLVXUWL',
                'label': 'Other resources',
                'has_biblio_sources': False,
            },
        ]

        # Make sure Zotero env values are set before proceeding.
        assert settings.ZOTERO_API_KEY
        assert settings.ZOTERO_API_KEY_GP
        assert settings.ZOTERO_LIBRARY_ID
        assert settings.ZOTERO_LIBRARY_ID_GP

        tenant = Tenant.objects.get(name='DALME')
        new_project = Project.objects.create(
            name='DALME',
            description='The Documentary Archaeology of Late Medieval Europe',
            zotero_library_id=int(settings.ZOTERO_LIBRARY_ID),
            zotero_api_key=settings.ZOTERO_API_KEY,
            tenant=tenant,
        )

        for collection in collections:
            collection.update(project=new_project)
            z_col = ZoteroCollection.objects.create(**collection)

            with schema_context('dalme'):
                log(instance=z_col, action='wagtail.create')

        # GP
        self.logger.info('Creating project and library entries for GP')
        tenant = Tenant.objects.get(name='Pharmacopeias')
        new_project = Project.objects.create(
            name='Pharmacopeias',
            description='Pharmacopeias',
            zotero_library_id=int(settings.ZOTERO_LIBRARY_ID_GP),
            zotero_api_key=settings.ZOTERO_API_KEY_GP,
            tenant=tenant,
        )

    @transaction.atomic
    def update_footnote_state(self):
        """Update footnote state fields for pages."""
        targets = [
            'collection',
            'collections',
            'essay',
            'featuredinventory',
            'featuredobject',
            'features',
            'flat',
        ]

        self.logger.info('Updating footnote state fields...')
        for model_name in targets:
            qualified_name = f'web_{model_name}'
            self.logger.info('Processing "%s"', qualified_name)
            with schema_context('dalme'):
                model = apps.get_model(app_label='web', model_name=model_name)
                for instance in model.objects.all():
                    raw_content = str(instance.body.raw_data)
                    instance.has_footnotes = 'data-footnote=' in raw_content
                    instance.has_placemarker = 'footnotes_placemarker' in raw_content
                    instance.save(update_fields=['has_footnotes', 'has_placemarker'])

    @transaction.atomic
    def fix_biblio_page(self):
        """Fix collection block references in bibliography page."""
        self.logger.info('Fixing collection block references in bibliography page')
        with schema_context('dalme'):
            from web.models import Bibliography

            biblio_page = Bibliography.objects.first()
            body = biblio_page.body.get_prep_value()
            for block in body:
                if block.get('type') == 'bibliography':
                    block['value'] = block['value']['collection']

            biblio_page.body = body
            biblio_page.save(update_fields=['body'])

    @transaction.atomic
    def replace_about_people(self):
        """Replace the About > People page with one that uses the new Team extension."""
        people_page_data = {
            'title': 'People',
            'short_title': 'People',
            'header_image_id': 11,
            'slug': 'people',
            'show_in_menus': True,
            'body': [
                {'id': 'eac3c1b6-6724-42af-a039-afef0ca8b880', 'type': 'heading', 'value': 'Project Team'},
                {
                    'id': '83f8d736-839d-407b-82ed-90e7ae981ccf',
                    'type': 'team_list',
                    'value': {
                        'mode': 'members',
                        'role': '',
                        'order': 'name',
                        'members': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
                    },
                },
                {'id': '61df150f-065e-4c33-b103-e5ae76991cc3', 'type': 'heading', 'value': 'Contributors'},
                {
                    'id': '447c0a2f-d127-4937-a72d-bb9644592883',
                    'type': 'team_list',
                    'value': {'mode': 'role', 'role': '3', 'order': 'name', 'members': []},
                },
                {'id': 'd91180b0-8a60-4c9b-8ed2-4b16fe840bec', 'type': 'heading', 'value': 'Advisory Board'},
                {
                    'id': 'c381034b-a89c-4df8-b578-40781dc24044',
                    'type': 'text',
                    'value': '<p data-block-key="khpxl">The members of the DALME board help convey news about the project to colleagues and students in the field and, in turn, bring potential contributors and resources to our attention.</p>',
                },
                {
                    'id': '89294881-07a3-4582-8a86-2733be10b447',
                    'type': 'team_list',
                    'value': {'mode': 'role', 'role': '4', 'order': 'name', 'members': []},
                },
            ],
        }

        self.logger.info('Replacing About > People page...')
        with schema_context('dalme'):
            from wagtail.models import Page

            from web.models import People

            # delete existing People page
            Page.objects.get(title='People').delete()

            # create new one
            about_page = Page.objects.get(title='About').specific
            people_page = about_page.add_child(instance=People(**people_page_data))
            people_page.save_revision().publish()

    @transaction.atomic
    def process_images(self):
        """Apply feature recognition to images and get rendition for people."""
        self.logger.info('Applying feature recognition to images and generating renditions...')
        with schema_context('dalme'):
            from wagtail.images import get_image_model

            Image = get_image_model()  # noqa: N806

            for image in Image.objects.all():
                try:
                    if not image.has_focal_point():
                        image.set_focal_point(image.get_suggested_focal_point())
                        image.save()
                        image.get_rendition('fill-100x100')
                except:  # noqa: E722
                    pass

    @transaction.atomic
    def add_default_preferences(self):
        """Create default user preferences."""
        default_preferences = [
            {
                'name': 'tooltipsOn',
                'label': 'Show Tooltips',
                'description': 'Turn UI tooltips on or off.',
                'data_type': 'bool',
                'group': 'IDA',
                'default': 'True',
            },
            {
                'name': 'sidebarCollapsed',
                'label': 'Collapse sidebar',
                'description': 'Collapse or expand the menu sidebar',
                'data_type': 'bool',
                'group': 'IDA',
                'default': 'False',
            },
            {
                'name': 'font_size',
                'label': 'Font size',
                'description': 'Size of the font in points.',
                'data_type': 'int',
                'group': 'Record Editor',
                'default': '14',
            },
            {
                'name': 'highlight_word',
                'label': 'Highlight words',
                'description': 'Highlight all instances of a word when selected.',
                'data_type': 'bool',
                'group': 'Record Editor',
                'default': 'True',
            },
            {
                'name': 'show_guides',
                'label': 'Guides',
                'description': 'Show/hide margin guides.',
                'data_type': 'bool',
                'group': 'Record Editor',
                'default': 'True',
            },
            {
                'name': 'show_gutter',
                'label': 'Gutter',
                'description': 'Show/hide the page gutter.',
                'data_type': 'bool',
                'group': 'Record Editor',
                'default': 'True',
            },
            {
                'name': 'show_invisibles',
                'label': 'Invisible characters',
                'description': 'Show/hide invisible characters.',
                'data_type': 'bool',
                'group': 'Record Editor',
                'default': 'False',
            },
            {
                'name': 'show_lineNumbers',
                'label': 'Line numbers',
                'description': 'Show/hide line numbers.',
                'data_type': 'bool',
                'group': 'Record Editor',
                'default': 'True',
            },
            {
                'name': 'soft_wrap',
                'label': 'Soft wrap',
                'description': 'Turn text soft wrapping on/off.',
                'data_type': 'bool',
                'group': 'Record Editor',
                'default': 'True',
            },
            {
                'name': 'theme',
                'label': 'Theme',
                'description': 'Change syntax colouring theme.',
                'data_type': 'str',
                'group': 'Record Editor',
                'default': 'Chrome',
            },
        ]

        self.logger.info('Creating default preferences...')
        for pref_obj in default_preferences:
            PreferenceKey.objects.create(**pref_obj)

    @transaction.atomic
    def migrate_corpora(self):
        """Migrate corpora from Wagtail to IDA."""
        self.logger.info('Migrating corpora...')

        tenant = Tenant.objects.get(name='DALME')

        with schema_context('dalme'):
            from web.extensions.records.models import Corpus

            User = get_user_model()  # noqa: N806
            user_obj = User.objects.get(pk=1)
            col_ct = ContentType.objects.get_for_model(Collection)
            corpora = Corpus.objects.all()

            for corpus in corpora:
                new_col = Collection.objects.create(
                    name=corpus.title,
                    is_corpus=True,
                    is_published=True,
                    tenant_id=tenant.id,
                )

                for member in corpus.collections.all():
                    CollectionMembership.objects.create(
                        collection_id=new_col.id,
                        content_type=col_ct,
                        object_id=member.record_collection_id,
                        tenant_id=tenant.id,
                        creation_user=user_obj,
                        modification_user=user_obj,
                    )
