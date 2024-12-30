"""Migrate public CMS data."""

import io
import json

from django_tenants.utils import schema_context
from psycopg import sql
from wagtail.log_actions import log

from django.apps import apps
from django.core.files import File
from django.db import connection, transaction
from django.db.utils import IntegrityError

from oauth.models import User

from .base import BaseStage
from .fixtures import GRADIENTS, ROLES

SOURCE_SCHEMA = 'restore'
CLONED_SCHEMA = 'cloned'


class Stage(BaseStage):
    """Data migration for public/cms models."""

    name = '11 Public/CMS'

    @transaction.atomic
    def apply(self):
        """Execute the stage."""
        self.clone_schema()
        self.move_django_site()
        self.drop_cloned_schema()
        self.migrate_wagtail_tables()
        self.migrate_public_tables()
        self.migrate_content_tables()
        self.create_footnotes()
        self.transfer_wagtail_user_profiles()
        self.transfer_snippets()
        self.transfer_gradients()
        self.migrate_people()
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
    def migrate_wagtail_tables(self):  # noqa: C901, PLR0912, RUF100
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
        skip = ['wagtailcore_uploadedfile', 'wagtailcore_revision', 'wagtailadmin_editingsession']

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
    def migrate_public_tables(self):  # noqa: C901, PLR0915, PLR0912, RUF100
        """Migrate existing Public tables to the DALME schema (BUT NOT INDICES)."""
        # we need to do these tables differently, i.e. by inserting data directly in SQL
        # because the constraints on foreign keys won't allow use of the ORM, for example
        # because all page types are subclassed from the wagtail Page model which we already
        # populated
        models = [
            ('webimages', 'baseimage'),
            ('webimages', 'customrendition'),
            ('wagtaildocs', 'document'),
            ('web', 'home'),
            ('web', 'section'),
            ('web', 'bibliography'),
            ('webrecords', 'corpus'),
            ('webrecords', 'corpus_collections'),
        ]

        banners_raw = None
        sponsors_raw = None

        self.logger.info('Processing additional models')
        for app, model_name in models:
            model = apps.get_model(app_label=app, model_name=model_name)
            with connection.cursor() as cursor:
                self.logger.info('Copying "%s"', f'{app}_{model_name}')
                target = f'{app}_{model_name}' if app.startswith('wag') else f'public_{model_name}'
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

                    if model_name == 'baseimage':
                        if 'description' in columns:
                            del columns[columns.index('description')]
                        columns.append('description')
                        values = values + ",''"

                    sql = f"INSERT INTO dalme.{app}_{model_name} ({', '.join(columns)}) VALUES ({values});"
                    cursor.execute(sql)

        if banners_raw:
            banner_data = json.loads(banners_raw)
            with schema_context('dalme'):
                from web.extensions.banners.models import Banner

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
                from web.models import Sponsor

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
    def migrate_content_tables(self):
        """Migrate Public/CMS tables with content that needs to be changed."""
        # these are tables with streamfields where content needs to be converted
        # between new and old formats, e.g. footnotes, references, people/team members
        # main/inline images, etc.

        models = [
            ('public', 'flat'),
            ('public', 'features'),
            ('public', 'collections'),
            ('public', 'collection'),
            ('public', 'essay'),
            ('public', 'featuredinventory'),
            ('public', 'featuredobject'),
            ('wagtailcore', 'revision'),
        ]

        self.logger.info('Processing models requiring content conversions')
        for app, model_name in models:
            is_rev = model_name == 'revision'

            with schema_context('dalme'):
                new_app_name = self.map_app(app)
                target = apps.get_model(app_label=new_app_name, model_name=model_name)
                target_fields = self.get_fields_by_type(target, ['JSONField', 'RichTextField'], as_map=True)

            with connection.cursor() as cursor:
                source = f'{app}_{model_name}'
                self.logger.info('Copying "%s"', source)
                cursor.execute(f'SELECT * FROM restore.{source};')
                rows = self.map_rows(cursor)
                for row in rows:
                    columns = []
                    values = ''
                    page_id = row.get('object_id') if is_rev else row.get('page_ptr_id')

                    for field_name in ['content_type_id', 'base_content_type_id']:
                        if row.get(field_name):
                            new_ct = self.map_content_type(row[field_name], id_only=True)
                            row[field_name] = new_ct

                            if is_rev and field_name == 'content_type_id':
                                content = json.loads(row['content'])
                                content['content_type'] = new_ct
                                row['content'] = json.dumps(content)

                    for idx, (name, value) in enumerate(row.items()):
                        columns.append(f'{name}')

                        if name == 'permission_id':
                            value = self.map_permissions(value)  # noqa: PLW2901

                        if name in target_fields:
                            value = self.process_content_field(value, target_fields[name], page_id, is_rev)  # noqa: PLW2901

                        # the value of certain field types has to be converted to account
                        # for differences in the way Django sets up certain fields depending
                        # on database backend. E.g. certain fields that are setup as varchar in MySQL
                        # are setup as jsonb in Postgres.
                        values += f'{self.clean_db_value(value, target._meta.get_field(name).get_internal_type())}'  # noqa: SLF001

                        if idx < len(row) - 1:
                            values += ', '

                    sql = f"INSERT INTO dalme.{new_app_name}_{model_name} ({', '.join(columns)}) VALUES ({values});"
                    cursor.execute(sql)

    @transaction.atomic
    def create_footnotes(self):
        """Create footnote entities extracted in previous stage."""
        if self.FOOTNOTES:
            with schema_context('dalme'):
                from wagtail.models import Page

                from web.extensions.footnotes.models import Footnote

                fn_objects = []
                for record in self.FOOTNOTES:
                    page = Page.objects.get(pk=record.pop('page_id'))
                    record['page'] = page
                    fn_objects.append(Footnote(**record))

                Footnote.objects.bulk_create(fn_objects)

    @transaction.atomic
    def transfer_wagtail_user_profiles(self):
        """Transfer user profiles from Wagtail."""
        with connection.cursor() as cursor:
            self.logger.info('Transfering user profiles from Wagtail')
            cursor.execute('SELECT * FROM restore.wagtailusers_userprofile;')
            rows = self.map_rows(cursor)
            created = 0
            transfered = 0

            with schema_context('public'):
                from wagtail.users.models import UserProfile

                for row in rows:
                    row.pop('id')
                    row.pop('dismissibles')
                    user = User.objects.filter(pk=row['user_id'])
                    if user.exists():
                        user = user.first()
                        avatar = row.pop('avatar')

                        if not avatar:
                            self.logger.warning('User %s has no avatar.', row['user_id'])
                        else:
                            photo = UserProfile.objects.get(user=user).avatar
                            user.avatar.save(photo.filename, File(io.BytesIO(photo.file.read())))
                            user.save(update_fields=['avatar'])
                            self.logger.debug('User %s: avatar updated.', row['user_id'])

                        if user.profile:
                            row.pop('user_id')
                            for field, value in row.items():
                                setattr(user.profile, field, value)
                            user.profile.save()
                            transfered += 1
                        else:
                            UserProfile.objects.create(**row)
                            created += 1
                    else:
                        self.logger.error(
                            'Failed to update profile for user "%s": user does not exist.', row['user_id']
                        )
            self.logger.debug('Transfered %s user profiles and created %s', transfered, created)

    @transaction.atomic
    def transfer_snippets(self):
        """Transfer snippet data to relevant tables and create settings."""
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
                from web.extensions.images.models import BaseImage
                from web.models import FooterLink, Settings, SocialMedia

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
                    team_profiles_url='/about/people/',
                    **settings,
                )

                for editor in [5, 1, 35]:  # smail, pizzorno, morreale
                    new_settings.editors.add(editor)

    @transaction.atomic
    def transfer_gradients(self):
        """Transfer gradient values and link page records."""
        self.logger.info('Transfering gradient data to DALME tenant')
        with schema_context('dalme'):
            from web.extensions.gradients.models import Gradient

            for entry in GRADIENTS:
                target_model = apps.get_model(app_label='web', model_name=entry.pop('model'))
                page_title = entry.pop('page_title', None)

                # create entry in gradients table
                gradient_obj = Gradient.objects.create(**entry)
                log(instance=gradient_obj, action='wagtail.create')

                # get page object
                page = target_model.objects.filter(title=page_title) if page_title else target_model.objects.all()

                if not page.exists():
                    self.logger.error('ERROR processing "%s": page does not exist.', entry['description'])
                    continue
                if page.count() > 1:
                    self.logger.error('ERROR processing "%s": query returns multiple pages.', entry['description'])
                    continue

                # add gradient reference
                page = page.first()
                page.gradient = gradient_obj
                page.save(update_fields=['gradient'])

    @transaction.atomic
    def migrate_people(self):  # noqa: C901, PLR0915
        """Convert people blocks to TeamMember entities."""
        with connection.cursor() as cursor:
            cursor.execute(sql.SQL('SELECT * FROM restore.public_flat WHERE page_ptr_id = 16;'))
            rows = self.map_rows(cursor)
            people_page = next(iter(rows))

        with schema_context('dalme'):
            from web.extensions.images.models import BaseImage
            from web.extensions.team.models import TeamMember, TeamRole

            self.logger.info('Creating TeamRole records...')
            roles = {k: TeamRole.objects.create(**v) for k, v in ROLES.items()}

            self.logger.info('Converting people blocks to TeamMember entities')
            for block in json.loads(people_page['body']):
                if block.get('type') == 'subsection':
                    block_value = block['value']
                    current_role = roles.get(block_value.get('subsection'))
                elif block.get('type') == 'person':
                    block_value = block['value']
                    name = block_value.get('name')
                    tm_object = {
                        'name': name,
                        'title': block_value.get('job'),
                        'defaults': {
                            'affiliation': block_value.get('institution'),
                            'url': block_value.get('url'),
                        },
                    }

                    user = self.user_match(name)
                    if user:
                        tm_object['user'] = user

                    photo_id = block_value.get('photo')
                    has_photo = False

                    try:
                        photo = BaseImage.objects.filter(pk=photo_id)
                        if photo.exists():
                            has_photo = True
                            photo = photo.first()
                            if user and not user.avatar:
                                user.avatar.save(photo.title, File(io.BytesIO(photo.file.read())))
                                user.save(update_fields=['avatar'])
                                self.logger.debug('Added avatar for user %s.', name)
                        else:
                            self.logger.error('No photo found for %s.', name)
                    except:  # noqa: E722
                        self.logger.error('%s: could not retrieve photo id=%s.', name, photo_id)  # noqa: TRY400

                    try:
                        tm, created = TeamMember.objects.get_or_create(**tm_object)
                        tm.roles.add(current_role)
                        if user and user.id in [1, 5]:
                            tm.roles.add(roles['PI'])
                        action = 'wagtail.create' if created else 'wagtail.edit'
                        log(instance=tm, action=action)

                    except IntegrityError:
                        tm = TeamMember.objects.get(user=user)
                        tm.roles.add(current_role)
                        self.logger.error('Found duplicate record for %s.', name)  # noqa: TRY400

                    if has_photo:
                        photo = BaseImage.objects.get(pk=photo_id)
                        tm.avatar.save(photo.title, File(io.BytesIO(photo.file.read())))
                        tm.save(update_fields=['avatar'])

            self.logger.error('Created %s TeamMember instances.', TeamMember.objects.count())

    @transaction.atomic
    def drop_restore_schema(self):
        """Drop the restore schema."""
        with connection.cursor() as cursor:
            self.logger.info("Dropping the '%s' schema", SOURCE_SCHEMA)
            cursor.execute('DROP SCHEMA restore CASCADE')
