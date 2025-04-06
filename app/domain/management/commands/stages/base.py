"""Base class for a data migration stage."""

import abc
import copy
import functools
import json
import re
import uuid

import lxml.etree as et
import markdown
import structlog
from bs4 import BeautifulSoup
from django_tenants.utils import schema_context

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db import connection

from domain.models import Agent, Attribute, AttributeType, EntityPhrase, LocaleReference, Location, Place, SavedSearch
from oauth.models import User

from .fixtures import (
    ALTERED_APP_MAP,
    ALTERED_MODEL_MAP,
    CONTENT_CLEANUP_EXPRESSIONS,
    ONE_OFF_TRANSFORMS,
    ORG_NAME_PATTERNS,
    PERSONAL_NAME_PATTERNS,
    PLACE_CONCORDANCE,
    REF_CITATIONS,
    RS_TYPES,
    SOURCES_MODEL_MAP,
    USER_NAME_CONCORDANCE,
)

logger = structlog.get_logger(__name__)

REFERENCE_HREF = re.compile(r'(?:(?:http|https)://dalme.org)?/?/project/bibliography/#([A-Z0-9]{8})')

# Here are some useful statements if you want to compare ContentType diffs.
# SELECT * FROM public.django_content_type new_ct INNER JOIN restore.django_content_type old_ct ON new_ct.model = old_ct.model;
# SELECT * FROM public.django_content_type new_ct INNER JOIN restore.django_content_type old_ct ON new_ct.model = old_ct.model
# WHERE new_ct.app_label != old_ct.app_label;


class MigrationError(Exception):
    """Raise this exception anywhere within a stage to abort the transaction."""


class BaseStage(abc.ABC):
    """Interface for a data migration stage."""

    FN_REGISTER = {}  # register to keep track of footnote indices
    FOOTNOTES = []  # storage for footnotes

    @abc.abstractmethod
    def apply(self):
        """Execute the migration stage."""
        ...

    @property
    def logger(self):
        """Provide the logger to all inheriting classes."""
        return logger

    @functools.cached_property
    def old_content_types_index(self):
        """Index the content types from the data being migrated."""
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM restore.django_content_type')
            rows = self.map_rows(cursor)

            index = {}
            for ct in rows:
                if (ct['app_label'], ct['model']) in ALTERED_MODEL_MAP:
                    # Let's just update these on the fly to the new values and
                    # it reduces the overall complexity of the transformation.
                    app_label, model = ALTERED_MODEL_MAP[(ct['app_label'], ct['model'])].split('.')
                else:
                    app_label, model = (ALTERED_APP_MAP.get(ct['app_label'], ct['app_label']), ct['model'])

                ct_id = ct['id']
                # Return the data as the key into the new_cts index.
                index[ct_id] = (app_label, model)

            return index

    @functools.cached_property
    def old_permissions_index(self):
        """Index the permissions from the data being migrated."""
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM restore.auth_permission')
            rows = self.map_rows(cursor)
        return {row['id']: (row['codename'], row['content_type_id']) for row in rows}

    @functools.cached_property
    def new_content_types_index(self):
        """Index the content types from the current db state."""
        index = {}
        for ct in ContentType.objects.all():
            app_label = ct.app_label
            model = ct.model
            key = (app_label, model)
            index[key] = {'id': ct.id, 'model': model, 'app_label': app_label}

        return index

    @staticmethod
    def map_rows(cursor):
        """Map db rows from tuples to dictionaries."""
        columns = [col[0] for col in cursor.description]
        return (dict(zip(columns, row, strict=True)) for row in cursor.fetchall())

    @staticmethod
    def get_fields_by_type(model, field_types, as_map=False):
        # Wagtail subclasses Django fields without redefining the method
        # or declaring the __name__ attribute
        # so for certain types we need to use the field's class instead
        # of calling field.get_internal_type()
        filter_by_class = ['RichTextField']

        if not isinstance(field_types, list):
            field_types = [field_types]

        target_types = [t for t in field_types if t not in filter_by_class]
        target_classes = [t for t in field_types if t in filter_by_class]

        fields = {}
        for field in model._meta.get_fields():  # noqa: SLF001
            try:
                field_cls_name = str(field.__class__)[8:-2].split('.')[-1]
                if field.get_internal_type() in target_types or field_cls_name in target_classes:
                    fields[field.name] = field.get_internal_type()
            except AttributeError:  # it's a GenericForeignKey
                continue
        return fields if as_map else list(fields.keys())

    def map_app(self, old_app_name):
        return ALTERED_APP_MAP.get(old_app_name, old_app_name)

    def map_content_type(self, old_id, id_only=False):
        """Map an old content type to a new content type."""
        if not old_id:
            return None
        if id_only and old_id in SOURCES_MODEL_MAP:
            key = SOURCES_MODEL_MAP[old_id]
            return self.new_content_types_index[key]['id']
        key = self.old_content_types_index[old_id]
        if id_only:
            return self.new_content_types_index[key]['id']
        return self.new_content_types_index[key]

    def map_permissions(self, old_id):
        auth_permission = apps.get_model(app_label='auth', model_name='permission')
        codename, old_ctype = self.old_permissions_index[old_id]
        target_ctype = self.map_content_type(old_ctype, id_only=True)
        return auth_permission.objects.get(codename=codename, content_type_id=target_ctype).id

    def clean_db_value(self, value, field_type):
        if value is None:
            return 'null'
        if field_type == 'JSONField':
            return f'$${value}$$::jsonb'
        if field_type in ['AutoField', 'BigAutoField', 'BigIntegerField', 'IntegerField']:
            return value if isinstance(value, int) else int(value)
        return f'$${value}$$'

    def markdown_to_html(self, content):
        # <span data-footnote=\"For Bons-Enfants, houses of poor grammar-school students attested across northern France and francophone Flanders (as Douai),
        # Joan M. Reitzel, &quot;[The Medieval House of Bons-Enfants](http://dalme.org/project/bibliography/#ZUMTQ5B9),&quot; _Viator_ 11 (1980): 179-207.\"
        # data-note_id=\"1fe36ff5-2e03-4890-82b1-71090d6333d7\">✱</span>
        soup = BeautifulSoup(markdown.markdown(content), features='lxml')
        references = soup.find_all('a', href=REFERENCE_HREF)
        if references:
            soup = self.convert_references(soup)

        return ''.join(str(b) for b in soup.body.findChildren(recursive=False))

    def convert_references(self, soup):
        for ref in soup.find_all('a', href=REFERENCE_HREF):
            # format: <a data-biblio="54" data-id="R476GUY2" data-reference="(Telliez, 2011)" linktype="reference">consumption</a>
            match = REFERENCE_HREF.fullmatch(ref['href'])
            if match:
                ref['data-biblio'] = self.biblio_page_id
                ref_id = match.group(1)
                try:
                    citation = REF_CITATIONS[ref_id]
                except KeyError:
                    citation = ''
                    self.logger.error('Reference id: %s not in citation list!', ref_id)  # noqa: TRY400
                ref['data-id'] = ref_id
                ref['data-reference'] = citation  # TODO: figure out a better way to get the citation!
                ref['linktype'] = 'reference'
                del ref['href']

        return soup

    def get_footnote_id(self, content, page_id):
        if self.FOOTNOTES:
            results = [i for i in self.FOOTNOTES if i['text'] == content and i['page_id'] == page_id]
            if results and len(results) == 1:
                return results[0]['id']
        return None

    def fix_entities(self, text, page_id, is_rev=False):
        soup = BeautifulSoup(text, features='lxml')

        # references
        references = soup.find_all('a', href=REFERENCE_HREF)
        if references:
            soup = self.convert_references(soup)

        # footnotes
        footnotes = soup.find_all('span', attrs={'data-footnote': True})
        if footnotes:
            fn_index = self.FN_REGISTER.get(page_id, 1)

            for idx, fn in enumerate(footnotes, start=fn_index):
                # format: <a data-footnote="c847f9da-3780-4085-9426-73e7a0228b3d" linktype="footnote">✱</a>
                fn_content = self.markdown_to_html(fn['data-footnote'])

                if is_rev:
                    # we don't create footnote records for page revisions as they would be repeats
                    # of notes that already exist in the live pages
                    fn_id = self.get_footnote_id(fn_content, page_id)
                    fn['data-footnote'] = fn_id if fn_id else True

                else:
                    new_footnote_id = uuid.uuid4()
                    self.FOOTNOTES.append(
                        {
                            'id': new_footnote_id,
                            'page_id': page_id,
                            'text': fn_content,
                            'sort_order': idx,
                        }
                    )

                    fn['data-footnote'] = new_footnote_id

                self.FN_REGISTER[page_id] = idx  # update footnote index for page with last used one
                fn.name = 'a'
                fn['linktype'] = 'footnote'
                del fn['data-note_id']

            self.FN_REGISTER[page_id] += 1  # increment last index by one for next run

        # saved searches
        # source format: <a id="01d5187e-2752-466e-9e7d-64e51051facd" linktype="saved_search">storage</a>
        # target format: <a id="01d5187e-2752-466e-9e7d-64e51051facd" data-saved-search="pansier" linktype="saved_search">dissemination</a>
        saved_searches = soup.find_all('a', attrs={'linktype': 'saved_search'})
        if saved_searches:
            for ss in saved_searches:
                try:
                    search_obj = SavedSearch.objects.get(pk=ss['id'])
                    ss['data-saved-search'] = search_obj.name
                except:  # noqa: E722
                    self.logger.error('Failed to migrate saved search entity in page %s', page_id)  # noqa: TRY400

        return ''.join(str(b) for b in soup.body.findChildren(recursive=False))

    def parse_streamfield(self, content, page_id, is_rev=False):  # noqa: C901, PLR0912, PLR0915
        """We parse streamfields to convert between content formats and convert the old subsection blocks into the new nested system."""
        new_content = []
        subsection = None
        nested_subsection = None
        for sblock in content:
            block = copy.deepcopy(sblock)
            if not isinstance(block, str) and block.get('type') in ['subsection', 'subsection_end_marker']:
                is_nested = block.get('value', {}).get('minor_heading') and subsection is not None

                if is_nested:
                    block['type'] = 'nested_subsection'
                    if nested_subsection:
                        if not subsection['value'].get('body'):
                            subsection['value']['body'] = [nested_subsection]
                        else:
                            subsection['value']['body'].append(nested_subsection)
                    nested_subsection = block

                else:
                    if nested_subsection and subsection:
                        if not subsection['value'].get('body'):
                            subsection['value']['body'] = [nested_subsection]
                        else:
                            subsection['value']['body'].append(nested_subsection)

                        nested_subsection = None

                    if subsection:
                        new_content.append(subsection)

                    subsection = block if block.get('type') == 'subsection' else None
            else:
                if isinstance(block, str):
                    pass
                elif block.get('type') == 'text' and block.get('value'):
                    block['value'] = self.fix_entities(block['value'], page_id, is_rev=is_rev)

                elif block.get('type') == 'inline_image':
                    if isinstance(block['value'], dict):
                        block['value']['use_file_caption'] = not block['value'].get('show_caption')
                    else:
                        self.logger.warning('Found inline image with int value: %s', block['value'])

                elif block.get('type') == 'main_image':
                    block['type'] = 'inline_image'
                    image_id = block['value']
                    block['value'] = {
                        'image': image_id,
                        'show_caption': True,
                        'use_file_caption': True,
                        'alignment': 'main',
                    }

                elif block.get('type') == 'heading' and block.get('value') and isinstance(block['value'], str):
                    block['value'] = {
                        'level': 'h1',
                        'heading': block['value'],
                    }

                if nested_subsection:
                    if not nested_subsection['value'].get('body'):
                        nested_subsection['value']['body'] = [block]
                    else:
                        nested_subsection['value']['body'].append(block)

                elif subsection:
                    if not subsection['value'].get('body'):
                        subsection['value']['body'] = [block]
                    else:
                        subsection['value']['body'].append(block)

                else:
                    new_content.append(block)

        if nested_subsection:
            if subsection:
                if not subsection['value'].get('body'):
                    subsection['value']['body'] = [nested_subsection]
                else:
                    subsection['value']['body'].append(nested_subsection)
            else:
                nested_subsection['type'] = 'subsection'
                new_content.append(nested_subsection)

        if subsection:
            new_content.append(subsection)

        return new_content

    def process_content_field(self, field_value, field_type, page_id, is_rev):
        if field_type == 'JSONField':
            field_value_json = json.loads(field_value)
            content = json.loads(field_value_json['body']) if is_rev else field_value_json
            new_content = self.parse_streamfield(content, page_id, is_rev=is_rev)

            if is_rev:
                field_value_json['body'] = new_content
                field_value = json.dumps(field_value_json)
            else:
                field_value = json.dumps(new_content)

        else:
            field_value = self.fix_entities(field_value, page_id)

        return field_value

    @functools.cached_property
    def biblio_page_id(self):
        with schema_context('dalme'):
            from web.models import Bibliography

            return Bibliography.objects.first().page_ptr_id

    def user_match(self, name):
        name = USER_NAME_CONCORDANCE.get(name, name)
        match = User.objects.filter(full_name=name)
        if match.exists():
            if match.count() != 1:
                self.logger.error('Name %s matches multiple users.', name)
            else:
                return match.get()
        return None

    @staticmethod
    def clean_rs_content(ent):
        et.strip_elements(ent, ['del', 'gap', 'space'], with_tail=False)
        content = ' '.join(ent.itertext()).strip()
        for p in CONTENT_CLEANUP_EXPRESSIONS:
            content = re.sub(p[0], p[1], content)

        return content if content else None

    @staticmethod
    def remove_rs_entity(ent):
        parent = ent.getparent()
        tail = ent.tail
        text = ent.text
        content = text if text else ''
        content += tail if tail else ''
        prev = ent.getprevious()
        if prev is not None:
            prev.tail = (prev.tail or '') + content
        else:
            parent.text = (parent.text or '') + content

        parent.remove(ent)

    @staticmethod
    def capitalize_string(result, ops):
        for op in ops:
            if op == 'cap_first':
                result = result[0].upper() + result[1:]

            if op == 'cap_name':
                tokens = result.split()
                if len(tokens) == 3:  # noqa: PLR2004
                    result = f'{tokens[0].capitalize()} {tokens[1]} {tokens[2].capitalize()}'
                elif len(tokens) == 2 and ("'" in result or '’' in result):  # noqa: PLR2004, RUF001
                    for sp in ["'", '’']:  # noqa: RUF001
                        if sp in result:
                            tokens = result.split(f'd{sp}')
                            result = f'{tokens[0].capitalize()} d’{tokens[1].capitalize()}'  # noqa: RUF001
                else:
                    tokens = [t.capitalize() for t in tokens]
                    result = ' '.join(tokens)

            if op == 'cap_org':
                skip = ['du', 'de']
                tokens = [t.strip() for t in result.split()]
                tokens = [t.capitalize() if t not in skip else t for t in tokens]
                result = ' '.join(tokens)

        return result

    @staticmethod
    def process_agent_element(el, match, type_id, ep_id):
        rs_type = RS_TYPES[type_id]
        wrapper = el.getparent()
        matched_text = match.group(0)
        wrapper_text = wrapper.text
        wrapper_tail = wrapper.tail
        in_tail = matched_text in wrapper_tail if wrapper_tail else False
        remainder_list = wrapper_tail.split(matched_text) if in_tail else wrapper_text.split(matched_text)

        if in_tail:
            new_tag = et.Element('rs', type=rs_type, key=str(ep_id))
            new_tag.text = matched_text
            wrapper.addnext(new_tag)
            if len(remainder_list):
                if len(remainder_list[0]):
                    wrapper.tail = remainder_list[0]
                if len(remainder_list) == 2 and len(remainder_list[1]):  # noqa: PLR2004
                    new_tag.tail = remainder_list[1]

        else:
            new_tag = et.SubElement(wrapper, 'rs', type=rs_type, key=str(ep_id))
            new_tag.text = matched_text

            if len(remainder_list):
                wrapper.text = remainder_list[0] if len(remainder_list[0]) else None
                new_tag.tail = remainder_list[1] if len(remainder_list[1]) else None

    def get_agent_name(self, text):
        name = text.strip()

        if name.lower().startswith('comun') or name.lower().startswith('homin'):
            result = self.capitalize_string(name, ['cap_first'])
            return (result, True)

        if name in ONE_OFF_TRANSFORMS:
            return (ONE_OFF_TRANSFORMS[name], False)

        for pattern in ORG_NAME_PATTERNS:
            match = pattern[0].match(name)
            if match:
                if pattern[1] is None:
                    result = match.group(0)
                else:
                    values = [match.group(i) for i in pattern[1][1]]
                    result = pattern[1][0].format(*values)

                result = self.capitalize_string(result, pattern[2]) if pattern[2] is not None else result
                return (result, True)

        for pattern in PERSONAL_NAME_PATTERNS:
            match = pattern[0].search(name)
            if match:
                if pattern[1] is None:
                    result = match.group(0)
                else:
                    values = [match.group(i) for i in pattern[1][1]]
                    result = pattern[1][0].format(*values)

                result = self.capitalize_string(result, pattern[2]) if pattern[2] is not None else result
                return (result, False)

        return (None, False)

    def clean_org_name(self, name):
        name = name.replace('-', ' ')
        return self.capitalize_string(name, ['cap_org'])

    @staticmethod
    def check_locus(string):
        return any(string.lower().startswith(w) for w in ['in', 'nel', 'item nel', 'sotto', 'certe', 'ancora'])

    @staticmethod
    def get_placename(string):
        place_data = PLACE_CONCORDANCE.get(string)
        if place_data is None:
            return None
        return place_data['name']

    @staticmethod
    def get_place(name):
        locale = LocaleReference.objects.filter(name=name)
        locale = locale.first() if locale.exists() else None
        place = Place.objects.filter(name=name)
        place = place.first() if place.exists() else None

        if place is not None and locale is not None:
            p_loc = place.location.attributes.filter(attribute_type__name='locale')
            if p_loc.exists() and p_loc.first().id == locale.id:
                return place

        if locale is None:
            return Place.objects.create(
                name=name,
                creation_user_id=1,
                modification_user_id=1,
            )

        location_ctype = ContentType.objects.get(app_label='domain', model='location')
        atype_locale = AttributeType.objects.get(name='locale')

        location = Attribute.objects.filter(
            content_type=location_ctype,
            attribute_type=atype_locale,
            value__value__id=str(locale.id),
        )
        location = location.first().content_object if location.exists() else None

        if location is None:
            location_type = 4  # locale
            location = Location.objects.create(
                location_type=location_type,
                creation_user_id=1,
                modification_user_id=1,
            )
            Attribute.objects.create(
                content_object=location,
                attribute_type=atype_locale,
                value=locale,
                creation_user_id=1,
                modification_user_id=1,
            )

        return Place.objects.create(
            name=name,
            location=location,
            creation_user_id=1,
            modification_user_id=1,
        )

    @staticmethod
    def get_agent(name, agent_type):
        # create Agent instance (if necessary)
        # check if exists : scope to record?
        agent, _created = Agent.objects.get_or_create(
            name=name,
            agent_type=agent_type,
            defaults={
                'creation_user_id': 1,
                'modification_user_id': 1,
            },
        )

        return agent

    def create_phrase(self, transcription, object_type, data=None):
        if object_type == 'agent':
            obj = self.get_agent(**data)
        elif object_type == 'place':
            obj = self.get_place(data['name'])
        else:
            obj = None

        payload = {
            'transcription': transcription,
            'creation_user_id': 1,
            'modification_user_id': 1,
        }
        if obj is not None:
            payload['content_object'] = obj

        ep = EntityPhrase.objects.create(**payload)
        return str(ep.id)
