"""Migrate public CMS data."""

import json

from django_tenants.utils import schema_context
from psycopg import sql
from wagtail.log_actions import log

from django.apps import apps
from django.db import connection, transaction

from .base import BaseStage

SOURCE_SCHEMA = 'restore'
CLONED_SCHEMA = 'cloned'


class Stage(BaseStage):
    """Data migration for public/cms models."""

    name = '10 Public/CMS'

    @transaction.atomic
    def apply(self):
        """Execute the stage."""
        self.clone_schema()
        self.move_django_site()
        self.drop_cloned_schema()
        self.migrate_wagtail_tables()
        self.migrate_public_tables()
        self.transfer_wagtail_user_profiles()
        self.transfer_snippets()
        self.transfer_gradients()
        self.drop_restore_schema()

    @transaction.atomic
    def clone_schema(self):
        """Clone the restore schema giving us data we can safely mutate."""
        with connection.cursor() as cursor:
            self.logger.info("Cloning the '%s' schema", SOURCE_SCHEMA)
            cursor.execute("SELECT clone_schema(%s, %s, 'DATA');", [SOURCE_SCHEMA, CLONED_SCHEMA])

    @transaction.atomic
    def move_django_site(self):
        """Migrate django.site table to the DALME schema (it's used by Wagtail)."""
        # TODO: this table is not created by regular migrations, hence it's missing in the
        # global pharmacopeias schema. Is it really necessary for Wagtail?
        with connection.cursor() as cursor:
            self.logger.info('Moving django_site table')
            cursor.execute('ALTER TABLE cloned.django_site SET SCHEMA dalme;')

    @transaction.atomic
    def drop_cloned_schema(self):
        """Drop the cloned schema restoring original symmetry."""
        with connection.cursor() as cursor:
            self.logger.info("Dropping the '%s' schema", CLONED_SCHEMA)
            cursor.execute('DROP SCHEMA cloned CASCADE')

    @transaction.atomic
    def migrate_wagtail_tables(self):  # noqa: C901
        """Migrate existing CMS tables to the DALME schema (BUT NOT INDICES)."""
        app_labels = [
            'taggit',
            'wagtailadmin',
            'wagtailcore',
            'wagtailembeds',
            'wagtailforms',
            'wagtailimages',
            'wagtailredirects',
        ]
        reset = [
            'wagtailcore_collection',
            'wagtailcore_groupapprovaltask',
            'wagtailcore_groupapprovaltask_groups',
            'wagtailcore_groupcollectionpermission',
            'wagtailcore_grouppagepermission',
            'wagtailcore_locale',
            'wagtailcore_page',
            'wagtailcore_site',
            'wagtailcore_task',
            'wagtailcore_workflow',
            'wagtailcore_workflowpage',
            'wagtailcore_workflowtask',
        ]
        no_bulk = ['wagtailcore_groupapprovaltask']
        skip = ['wagtailcore_uploadedfile']

        # delete existing records
        with connection.cursor() as cursor:
            self.logger.info('Deleting existing records in dalme schema')
            for table in reset:
                cursor.execute(sql.SQL('TRUNCATE "dalme".{} RESTART IDENTITY CASCADE;').format(sql.Identifier(table)))

        for label in app_labels:
            self.logger.info('Processing "%s" models', label)
            app_config = apps.get_app_config(label)
            if app_config.models_module is not None:
                for model in app_config.get_models():
                    model_name = model.__name__.lower()
                    qualified_name = f'{label}_{model_name}'
                    if qualified_name not in skip:
                        self.logger.info('Copying "%s"', qualified_name)
                        use_bulk = qualified_name not in no_bulk
                        json_fields = self.get_fields_by_type(model, 'JSONField')

                        with connection.cursor() as cursor:
                            cursor.execute(
                                sql.SQL('SELECT * FROM "restore".{};').format(sql.Identifier(qualified_name))
                            )
                            rows = self.map_rows(cursor)

                        with schema_context('dalme'):
                            target_model = apps.get_model(app_label=label, model_name=model_name)
                            objs = []
                            for row in rows:
                                for field_name in ['content_type_id', 'base_content_type_id']:
                                    if row.get(field_name):
                                        new_ct = self.map_content_type(row[field_name], id_only=True)
                                        row[field_name] = new_ct

                                        if model_name == 'revision' and field_name == 'content_type_id':
                                            content = json.loads(row['content'])
                                            content['content_type'] = new_ct
                                            row['content'] = json.dumps(content)

                                if row.get('permission_id'):
                                    row['permission_id'] = self.map_permissions(row['permission_id'])

                                if json_fields:
                                    for field in json_fields:
                                        row[field] = json.loads(row[field])
                                if use_bulk:
                                    objs.append(target_model(**row))
                                else:
                                    target_model.objects.create(**row)

                            if use_bulk:
                                target_model.objects.bulk_create(objs)

    @transaction.atomic
    def migrate_public_tables(self):  # noqa: C901, PLR0915
        """Migrate existing Public tables to the DALME schema (BUT NOT INDICES)."""
        # we need to do these tables differently, i.e. by inserting data directly in SQL
        # because the constraints on foreign keys won't allow use of the ORM, for example
        # because all page types are subclassed from the wagtail Page model which we already
        # populated
        models = [
            ('dalme', 'publicimages', 'baseimage'),
            ('dalme', 'publicimages', 'customrendition'),
            ('dalme', 'wagtaildocs', 'document'),
            ('dalme', 'public', 'home'),
            ('dalme', 'public', 'section'),
            ('dalme', 'public', 'flat'),
            ('dalme', 'public', 'features'),
            ('dalme', 'public', 'bibliography'),
            ('dalme', 'public', 'collections'),
            ('dalme', 'public', 'collection'),
            ('dalme', 'publicrecords', 'corpus'),
            ('dalme', 'publicrecords', 'corpus_collections'),
            ('dalme', 'public', 'essay'),
            ('dalme', 'public', 'featuredinventory'),
            ('dalme', 'public', 'featuredobject'),
        ]

        banners_raw = None
        sponsors_raw = None

        self.logger.info('Processing additional models')
        for schema, app, model_name in models:
            model = apps.get_model(app_label=app, model_name=model_name)
            with connection.cursor() as cursor:
                self.logger.info('Copying "%s"', f'{app}_{model_name}')
                target = f'{app}_{model_name}' if app.startswith('w') else f'public_{model_name}'
                cursor.execute(f'SELECT * FROM restore.{target};')
                rows = self.map_rows(cursor)

                for row in rows:
                    columns = []
                    values = ''
                    for idx, (field, value) in enumerate(row.items()):
                        if model_name == 'home' and field == 'banners':
                            banners_raw = value
                        elif model_name == 'home' and field == 'sponsors':
                            sponsors_raw = value
                        else:
                            columns.append(f'{field}')
                            # the value of certain field types has to be converted to account
                            # for differences in the way Django sets up certain fields depending
                            # on database backend. E.g. certain fields that are setup as varchar in MySQL
                            # are setup as jsonb in Postgres.
                            values += f'{self.clean_db_value(value, model._meta.get_field(field).get_internal_type())}'  # noqa: SLF001
                            if idx < len(row) - 1:
                                values += ', '

                    if model_name == 'corpus':
                        columns.append('collapsed')
                        values = values + ',False'

                    sql = f"INSERT INTO {schema}.{app}_{model_name} ({', '.join(columns)}) VALUES ({values});"
                    cursor.execute(sql)

        if banners_raw:
            banner_data = json.loads(banners_raw)
            with schema_context('dalme'):
                from public.extensions.banners.models import Banner

                for banner in banner_data:
                    value = banner.get('value')
                    if value:
                        value.pop('page')
                        value['show_title'] = True
                        new_banner = Banner.objects.create(**value)

                        log(instance=new_banner, action='wagtail.create')

        if sponsors_raw:
            sponsor_data = json.loads(sponsors_raw)
            with schema_context('dalme'):
                from public.models import Sponsor

                for block in sponsor_data:
                    if block.get('type') == 'sponsors':
                        value = block['value']
                        url = value['url']
                        if 'acls' in url:
                            name = 'ACLS'
                        elif 'ias' in url:
                            name = 'Institute for Advanced Studies'
                        elif 'sohp' in url:
                            name = 'SOHP'
                        else:
                            name = "Dean's Competitive Fund"

                        new_sponsor = Sponsor.objects.create(name=name, url=url, logo_id=value['logo'])

                        log(instance=new_sponsor, action='wagtail.create')

    @transaction.atomic
    def transfer_wagtail_user_profiles(self):
        """Transfer user profiles from Wagtail."""
        with connection.cursor() as cursor:
            self.logger.info('Transfering user profiles from Wagtail')
            cursor.execute('SELECT * FROM restore.wagtailusers_userprofile;')
            rows = self.map_rows(cursor)
            with schema_context('public'):
                from wagtail.users.models import UserProfile

                for row in rows:
                    row.pop('id')
                    row.pop('dismissibles')
                    profile = UserProfile.objects.filter(user=row['user_id'])
                    if profile.exists():
                        row.pop('user_id')
                        profile.update(**row)
                    else:
                        UserProfile.objects.create(**row)

    @transaction.atomic
    def transfer_snippets(self):
        """Transfer snippet data to relevant tables."""
        footer_links = None
        footer_social = None
        settings = {}

        # GET DATA
        with connection.cursor() as cursor:
            self.logger.info('Transfering snippet data')

            # FOOTER DATA
            cursor.execute('SELECT * FROM restore.public_footer;')
            row = next(self.map_rows(cursor))
            footer_links = row['pages']
            footer_social = row['social']

            # SETTINGS DATA
            # searchpage
            cursor.execute('SELECT * FROM restore.public_searchpage;')
            row = next(self.map_rows(cursor))
            settings.update(
                {
                    'search_help_content': row['help_content'],
                    'search_header_image': row['header_image_id'],
                    'search_header_position': row['header_position'],
                }
            )
            # explorepage
            cursor.execute('SELECT * FROM restore.public_explorepage;')
            row = next(self.map_rows(cursor))
            settings.update(
                {
                    'explore_text_before': row['text_before'],
                    'explore_text_after': row['text_after'],
                    'explore_header_image': row['header_image_id'],
                    'explore_header_position': row['header_position'],
                }
            )
            # recordbrowser
            cursor.execute('SELECT * FROM restore.public_recordbrowser;')
            row = next(self.map_rows(cursor))
            settings.update(
                {
                    'browser_header_image': row['header_image_id'],
                    'browser_header_position': row['header_position'],
                }
            )
            # recordviewer
            cursor.execute('SELECT * FROM restore.public_recordviewer;')
            row = next(self.map_rows(cursor))
            settings.update(
                {
                    'viewer_header_image': row['header_image_id'],
                    'viewer_header_position': row['header_position'],
                }
            )

            # CREATE NEW RECORDS
            with schema_context('dalme'):
                from public.extensions.images.models import BaseImage
                from public.models import FooterLink, Settings, SocialMedia

                # FOOTER LINKS
                link_data = json.loads(footer_links)
                for block in link_data:
                    if block.get('type') == 'page':
                        value = block['value']
                        footer_link = FooterLink.objects.create(label=value['title'], page_id=value['page'])

                        log(instance=footer_link, action='wagtail.create')

                # SOCIAL MEDIA LINKS
                social_data = json.loads(footer_social)
                for block in social_data:
                    if block.get('type') == 'social':
                        value = block['value']
                        url = value['url']
                        name = 'Twitter/X' if 'twitter' in url else 'Facebook' if 'facebook' in url else 'Share'
                        SocialMedia.objects.create(
                            name=name, icon=value['fa_icon'], css_class=value['css_class'], url=url
                        )

                # SETTINGS
                settings.update(
                    {
                        'search_header_image': BaseImage.objects.get(pk=settings['search_header_image']),
                        'explore_header_image': BaseImage.objects.get(pk=settings['explore_header_image']),
                        'browser_header_image': BaseImage.objects.get(pk=settings['browser_header_image']),
                        'viewer_header_image': BaseImage.objects.get(pk=settings['viewer_header_image']),
                    }
                )

                new_settings = Settings.objects.create(
                    name='DALME',
                    short_form='DALME',
                    tagline='The Documentary Archaeology of Late Medieval Europe',
                    logo='images/dalme_logo.svg',
                    copyright_line='The Documentary Archaeology of Late Medieval Europe',
                    analytics_domain='dalme.org',
                    contact_email='projectdalme@gmail.com',
                    publication_title='The Documentary Archaeology of Late Medieval Europe',
                    publication_url='https://dalme.org',
                    search_tagline='DALME Corpora and Collections',
                    explore_tagline='DALME Corpora and Collections',
                    **settings,
                )

                for editor in [5, 1, 35]:  # smail, pizzorno, morreale
                    new_settings.editors.add(editor)

    @transaction.atomic
    def transfer_gradients(self):
        """Transfer gradient values and link page records."""
        gradients = [
            {
                'colour_1': '#064e8c80',
                'colour_2': '#114a2880',
                'angle': '125',
                'description': 'Homepage header',
                'model': 'home',
            },
            {
                'colour_1': '#5386a0b3',
                'colour_2': '#3f6544e6',
                'angle': '125',
                'description': 'Project section headers',
                'model': 'section',
                'page_title': 'Project',
            },
            {
                'colour_1': '#63623ab3',
                'colour_2': '#8a4747e6',
                'angle': '125',
                'description': 'Features section headers',
                'model': 'features',
            },
            {
                'colour_1': '#5f516fb3',
                'colour_2': '#173e65e6',
                'angle': '125',
                'description': 'Collections section headers',
                'model': 'collections',
            },
            {
                'colour_1': '#69663f99',
                'colour_2': '#926a10e6',
                'angle': '125',
                'description': 'About section headers',
                'model': 'section',
                'page_title': 'About',
            },
        ]
        self.logger.info('Transfering gradient data')
        with schema_context('dalme'):
            from public.extensions.gradients.models import Gradient

            for entry in gradients:
                target_model = apps.get_model(app_label='public', model_name=entry.pop('model'))
                page_title = entry.pop('page_title', None)

                # create entry in gradients table
                gradient_obj = Gradient.objects.create(**entry)
                log(instance=gradient_obj, action='wagtail.create')

                # get page object
                page = target_model.objects.filter(title=page_title) if page_title else target_model.objects.all()

                if not page.exists():
                    self.logger.info('ERROR processing "%s": page does not exist.', entry['description'])
                    continue
                if page.count() > 1:
                    self.logger.info('ERROR processing "%s": query returns multiple pages.', entry['description'])
                    continue

                # add gradient reference
                page = page.first()
                page.gradient = gradient_obj
                page.save(update_fields=['gradient'])

    @transaction.atomic
    def drop_restore_schema(self):
        """Drop the restore schema."""
        with connection.cursor() as cursor:
            self.logger.info("Dropping the '%s' schema", SOURCE_SCHEMA)
            cursor.execute('DROP SCHEMA restore CASCADE')
